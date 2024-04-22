import pathlib
import pandas
import rdflib
import owlrl
from rdflib import RDF, RDFS, OWL, URIRef

import selftest
test = selftest.get_tester(__name__)

testdatadir = pathlib.Path(__file__).parent.parent/'data'


class Object:
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
        return [Object(p, self.graph).name() for p in properties]


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
        # calculate closure as to have access to all inherited classes and properties
        owlrl.DeductiveClosure(owlrl.CombinedClosure.RDFS_OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)
        return graph

    def count_triples(self):
        return len(self.graph)

    def get_classes(self):
        return list(Object(uri, self.graph) for uri in self.graph[:rdflib.RDF.type: rdflib.OWL.Class])

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
    #test.eq(1748, ontology.count_triples())
    test.eq(11019, ontology.count_triples())
    classes =  ontology.get_classes()
    #test.eq(124, len(classes))
    test.eq(278, len(classes))
    class_names = [clazz.name() for clazz in classes]
    #test.eq({'http://purl.org/dc/terms/LinguisticSystem',
    #         'http://www.w3.org/2004/02/skos/core#Concept',
    #         'https://saref.etsi.org/core/FeatureOfInterest',
    #         'http://schema.org/Person',
    #         'http://www.w3.org/2002/07/owl#Nothing',   # from OWL expansion
    #         'http://www.w3.org/2002/07/owl#Thing'},    # idem
    #    set([clazz.uri.toPython() for clazz in classes if clazz.name() is None]),
    #    diff=test.diff2)

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
    properties = {c.name(): c.get_propertynames() for c in classes}
    test.eq([], properties['Chloramine sensor'])
    test.eq(118, len(properties))
    #test.eq( 95, len([name for name, props in properties.items() if props == []]))
    test.eq(['Analysis Results', 'Analysis Results Pipe', 'Earth Quake', 'Hazard Event', 'Hazard Parameter', 'Material', 'Physical component',
        'Risk Scenario', 'Service zone', 'Water network', 'Feature', 'SpatialObject', 'Device', 'Measurement', 'System', 'Consumption-based tariff',
        'Main', 'Pipe', 'Tariff', 'Threshold-based tariff', 'Time-based tariff', 'Transport asset', 'Water asset'],
     [name for name, props in properties.items() if props and name],
     diff=test.diff2)
    test.eq(['has joint material', 'has lining', 'has material', 'has cathodic', 'has diameter', 'has installation date', 
             'has joint type', 'has length', 'use type'], properties['Pipe'])
    test.eq(['has results pipe', 'expected repair cost distribution pipes', 'expected repair cost trans pipes', 'expected repair cost network', 'expected repair num distribution pipes', 'expected repair num network', 'expected repair num trans pipes', 'expected repair time distribution pipes', 'expected repair time network', 'expected repair time trans pipes'],
        properties['Analysis Results'])
    print("=== classes without properties ===")
    for cn, cp in properties.items():
        if not cp:
            print(cn)
    test.truth(False)



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

