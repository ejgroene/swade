import pathlib
import selftest
test = selftest.get_tester(__name__)
import pandas as pd
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef
from sentence_transformers import SentenceTransformer, util


testdatadir = pathlib.Path(__file__).parent.parent/'data'


def get_csv_table_names(directory_path):
    return [f.stem for f in directory_path.glob('*.csv')]


def get_columns_names(file_path):
    df = pd.read_csv(file_path)
    return [s.strip() for s in df.columns.tolist()]

class Ontology:
    def __init__(self, path, m="all-MiniLM-L6-v2"):
        self.graph = self.read_ontologies(path)
        self.st_model = SentenceTransformer(m)

    def read_ontologies(self, path):
        graph = rdflib.Graph()
        for f in path.glob('*.ttl'):
            graph.parse(f)
        return graph

    def count_triples(self):
        return len(self.graph)

    def get_classes(self):
        return list(self.graph[:rdflib.RDF.type: rdflib.OWL.Class])

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
def get_table_names_for_two_files(tmp_path):
    table = tmp_path/'tableA.csv'
    table.write_text("a, b, c\n 1, 2, 3\n")
    table_names = get_csv_table_names(tmp_path)
    test.eq(['tableA'], table_names)


@test
def get_columns_names_for_simple_files(tmp_path):
    some_file = tmp_path/'myfile.cvs'
    some_file.write_text("a, b, c\n 1, 2, 3\n")
    columns = get_columns_names(some_file.as_posix())
    test.eq(['a', 'b', 'c'], columns)


@test
def real_data():
    """ test to verify the functions with real data """
    table_names = get_csv_table_names(testdatadir)
    test.eq(['Pipe_city_b', 'city_A_pip'], table_names)
    column_names0 = get_columns_names(testdatadir/f"{table_names[0]}.csv")
    test.eq(['record_no', 'syszone', 'use_type', 'inst_date', 'material', 'joint', 'joint_type', 'cathodic', 'diameter', 'length_ft'], column_names0)
    column_names1 = get_columns_names(testdatadir/f"{table_names[1]}.csv")
    test.eq(['id', 'uid', 'zone', 'use_type', 'installed', 'material', 'joint', 'lining', 'diameter', 'd_cat', 'length_m'], column_names1)
    test.eq({'joint', 'material', 'use_type', 'diameter'}, set(column_names0) & set(column_names1))


@test
def read_ontology_real_data():
    """ test to verify the functions with real data """
    test.eq(1576, ontology.count_triples())
    classes =  ontology.get_classes()
    test.eq(108, len(classes))
    # find all text components of classes (label or comment)

@test
def get_terms():
    terms = ontology.get_terms('https://saref.etsi.org/saref4watr/Pipe')
    test.eq('Pipe: A pipe is a passage of water flowing in a closed conduit (i.e., not subject to atmospheric pressure).', terms)
    terms = ontology.get_terms(URIRef('https://saref.etsi.org/saref4watr/Pipe'))
    test.eq('Pipe: A pipe is a passage of water flowing in a closed conduit (i.e., not subject to atmospheric pressure).', terms)

#@test
def get_embeddings_for_class():
    """ this is a bit longrunning for a unit test """
    embeddings = ontology.get_embeddings('https://saref.etsi.org/saref4watr/Pipe')
    test.eq(384, len(embeddings))


# @test
# def get_match():
#     trible = {[s,p,o],}
#     tables_names ={['table1']}
#     column_names={table:[col1,colm1,], table:[col]}
#     match_table_className={[table:classn], ...}
#     result = match_table_className({data})
#     test.eq('classA', result)