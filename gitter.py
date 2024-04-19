import pathlib
from pathlib import Path
import selftest
test = selftest.get_tester(__name__)
import pandas as pd
import rdflib
from rdflib import RDF, RDFS, OWL
from sentence_transformers import SentenceTransformer, util
#from gensim.models import Word2Vec


directory_path = Path(r'C:\Users\gg363d\Source\Repos\swade\data')


def get_csv_table_names(directory_path):
    #print(directory_path)
    return [f.stem for f in directory_path.glob('*.csv')]

def get_columns_names(directory_path):
    column_names_per_table = {}
    table_names = get_csv_table_names(directory_path)  # Use directory_path here

    for table_name in table_names:
        file_path = directory_path / (table_name + ".csv")
        df = pd.read_csv(file_path)
        column_names_per_table[table_name] = [s.strip() for s in df.columns.tolist()]

    return column_names_per_table


def get_ontology(directory_path):
    ontology = rdflib.Graph()
    for f in directory_path.glob('*.ttl'):
        ontology.parse(f)
    return ontology



# def get_class_names(directory_path):
#     ontology = rdflib.Graph()
#     for f in directory_path.glob('*.ttl'):
#         ontology.parse(f)
    
#     class_names = set()  # Using a set to ensure unique class names
    
#     # Iterate over triples and extract class names
#     for s, p, o in ontology:
#         if p == rdflib.RDF.type and isinstance(o, rdflib.URIRef):
#             class_names.add(o)
        
#         # Extract classes from subclass relationships
#         if p == rdflib.RDFS.subClassOf and isinstance(s, rdflib.URIRef):
#             class_names.add(s)
    
#     return class_names



def get_class_names(directory_path):
    ontology = rdflib.Graph()
    for f in directory_path.glob('*.ttl'):
        ontology.parse(f)
    
    class_names = set()  # Using a set to ensure unique class names
    
    # Iterate over triples and extract class names
    for s, p, o in ontology:
        if p == rdflib.RDF.type and isinstance(o, rdflib.URIRef):
            class_names.add(rdflib.namespace.split_uri(o)[1])  # Extract local name
        
        # Extract classes from subclass relationships
        if p == rdflib.RDFS.subClassOf and isinstance(s, rdflib.URIRef):
            class_names.add(rdflib.namespace.split_uri(s)[1])  # Extract local name

    #[s.strip() for s in class_names]
    return class_names

# def get_class_names(directory_path):
#     ontology = rdflib.Graph()
#     for f in directory_path.glob('*.ttl'):
#         ontology.parse(f)
#     classes =  list(ontology[:rdflib.RDF.type: rdflib.OWL.Class])
    
#    return classes


def get_embeddings (names_list):

    #model = Word2Vec(sentences=[names_list], vector_size=100, window=5, min_count=1, workers=4)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = model.encode(names_list)
      
    return vectors


# test1 = get_columns_names(directory_path)
# print (len(test1))
# test2 = get_csv_table_names(directory_path)
# print (test1)

#test3 = get_ontology(directory_path)
#len will give the number of triple
#print (len(test3))

test4 = get_class_names(directory_path)
print(type(test4))

vectors = get_embeddings(list(test4))
print (vectors)