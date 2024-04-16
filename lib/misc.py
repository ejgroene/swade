import pathlib
import pandas
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef

import selftest
test = selftest.get_tester(__name__)

testdatadir = pathlib.Path(__file__).parent.parent/'data'


class Class:
    """ Represents a class from the ontology """
    def __init__(self, uri, graph):
        self.uri = uri
        self.graph = graph

    def name(self):
        labels = list(self.graph[self.uri: RDFS.label: None])
        if len(labels) > 0:
            return labels[0].toPython()
        return None

    def get_propertynames(self):
        properties = self.graph[None: RDFS.domain: self.uri]
        # unfortunately, no labels are given for properties
        return [p.toPython() for p in properties]


class Ontology:
    def __init__(self, path, m=None):
        self.graph = self.read_ontologies(path)
        if m:
            # only do this when requested; it is too slow
            from sentence_transformers import SentenceTransformer, util
            self.st_model = SentenceTransformer(m)

    def __len__(self):
        return len(self.get_classes())

    def read_ontologies(self, path):
        graph = rdflib.Graph()
        for f in path.glob('*.ttl'):
            graph.parse(f)
        return graph

    def count_triples(self):
        return len(self.graph)

    def get_classes(self):
        return list(Class(uri, self.graph) for uri in self.graph[:rdflib.RDF.type: rdflib.OWL.Class])

    def get_terms(self, class_uri):
        if not isinstance(class_uri, URIRef):
            class_uri = URIRef(class_uri)
        label, description = list(l.toPython() for l in self.graph[class_uri: RDFS.label | RDFS.comment])
        return f"{label}: {description}"

    def get_embeddings(self, uri):
        terms = self.get_terms(uri)
        return self.st_model.encode(terms)

ontology = Ontology(testdatadir)


@test
def read_ontology_real_data():
    """ test to verify the functions with real data """
    test.eq(1576, ontology.count_triples())
    classes =  ontology.get_classes()
    test.eq(108, len(classes))
    test.eq([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        'Public Service', 'Feature', 'Geometry', 'SpatialObject', 'Point', None, 'Instant', 'A temporal entity with an extent or duration',
        'Temporal duration', 'Temporal entity', 'Organization', 'Agent', 'Person', 'Actuator', 'Device', None, 'Measurement', 'Property',
        'Sensor', 'Unit of measure', 'Administrative area', 'Agent', 'City', 'City object', 'Country', 'District', 'Event', 'Facility', 
        'Key Performance Indicator', 'Key performance indicator assessment', 'Neighbourhood', 'Public administration', 'Public service',
        None, None, 'Point', 'Polygon', 'Day of week', 'Meter', 'System', 'Acceptability property', 'Aquifer', 'Bacterial property',
        'Channel', 'ChemicalProperty', 'Consumption-based tariff', 'Distribution system', 'Environmental property', 'Estuary', 
        'Fire hydrant', 'Gauging station', 'Glacier', 'Hydroelectric power plant', 'Intake', 'Lagoon', 'Lake', 'Main', 'Maintenance hole',
        'Microbial property', 'Monitoring infrastructure', 'Ocean', 'Pipe', 'Pit', 'Pump', 'Reservoir', 'River', 'Sea', 'Sink asset',
        'Source asset', 'Storage asset', 'Storage infrastructure', 'Tank', 'Tariff', 'Threshold-based tariff', 'Time-based tariff',
        'Transport asset', 'Treatment plant', 'Valve', 'Vent', 'Water', 'Water asset', 'Water device', 'Water flow property',
        'Water infrastructure', 'Water meter', 'Water meter property', 'Water property', 'Water use'],
    [clazz.name() for clazz in classes])
    # uncomment to see URIs without rdfs.label
    #test.eq([], [clazz.uri.toPython() for clazz in classes if clazz.name() is None])

@test
def get_terms():
    terms = ontology.get_terms('https://saref.etsi.org/saref4watr/Pipe')
    test.eq('Pipe: A pipe is a passage of water flowing in a closed conduit (i.e., not subject to atmospheric pressure).', terms)
    terms = ontology.get_terms(URIRef('https://saref.etsi.org/saref4watr/Pipe'))
    test.eq('Pipe: A pipe is a passage of water flowing in a closed conduit (i.e., not subject to atmospheric pressure).', terms)

#@test
def get_embeddings_for_class():
    """ this is a bit longrunning for a unit test """
    ontology = Ontology(m="all-MiniLM-L6-v2")
    embeddings = ontology.get_embeddings('https://saref.etsi.org/saref4watr/Pipe')
    test.eq(384, len(embeddings))

@test
def get_names_of_properties():
    classes = ontology.get_classes()
    for clazz in classes:
        properties = clazz.get_propertynames()
        test.eq([], properties)





class Table:
    """ Represents a table read from a .CSV file """
    def __init__(self, path):
        self.table_name = path.stem
        self.table = pandas.read_csv(path)

    def get_column_names(self):
        return [s.strip() for s in self.table.columns.tolist()]

    def name(self):
        return self.table_name


def read_tables(path):
    return [Table(f) for f in path.glob('*.csv')]


@test
def get_table_names_for_two_files(tmp_path):
    table = tmp_path/'tableA.csv'
    table.write_text("a, b, c\n 1, 2, 3\n")
    tables = read_tables(tmp_path)
    test.eq(1, len(tables))
    test.eq(['tableA'], [table.name() for table in tables])


@test
def get_columns_names_for_simple_files(tmp_path):
    some_file = tmp_path/'myfile.csv'
    some_file.write_text("a, b, c\n 1, 2, 3\n")
    tables = read_tables(tmp_path)
    test.eq(1, len(tables))
    columns = tables[0].get_column_names()
    test.eq(['a', 'b', 'c'], columns)


@test
def real_data():
    """ test to verify the functions with real data """
    tables = read_tables(testdatadir)
    test.eq(['Pipe_city_b', 'city_A_pip'], [table.name() for table in tables])
    column_names0 = tables[0].get_column_names()
    test.eq(['record_no', 'syszone', 'use_type', 'inst_date', 'material', 'joint', 'joint_type', 'cathodic', 'diameter', 'length_ft'], column_names0)
    column_names1 = tables[1].get_column_names()
    test.eq(['id', 'uid', 'zone', 'use_type', 'installed', 'material', 'joint', 'lining', 'diameter', 'd_cat', 'length_m'], column_names1)
    test.eq({'joint', 'material', 'use_type', 'diameter'}, set(column_names0) & set(column_names1))

