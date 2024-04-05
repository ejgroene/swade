from rdflib import Graph, RDFS, Literal
from rdflib.plugins.serializers.jsonld import Serializer
import getViector

directory_path = r'C:\Users\gg363d\Source\Repos\swade\data'

# Load the TTL file into an RDF graph
classes = graph = Graph()
graph.parse(location="swade.ttl", format="turtle")
graph.parse(location="saref4city.ttl", format="turtle")
graph.parse(location="saref4watr.ttl", format="turtle")

def get_jsonLD (graph):
    # Serialize the graph to JSON-LD format
    jsonld_data = graph.serialize(format='json-ld', indent=4)

    # Save or print the JSON-LD data
    with open("json_ld_output.jsonld", "w") as jsonld_file:
        jsonld_file.write(jsonld_data)

    #print(jsonld_data)

    return jsonld_data


def get_ontology_namespace(graph):

    # Iterate over triples to find namespace declarations
    namespaces = {}
    for _, predicate, obj in graph:
        if str(predicate) == "@prefix":
            # Extract namespace prefix and URI
            prefix, uri = str(obj).split()
            # Remove angle brackets from URI
            uri = uri.strip("<>")
            namespaces[prefix] = uri
    #print (namespaces)
    return namespaces




def get_ontology_namespace2(graph):
  

    # Get namespaces from the graph object
    #namespaces = dict(graph.namespaces())
    namespaces = list(graph.namespaces())

    return namespaces


ontology_namespaces = get_ontology_namespace2(graph)

#for prefix, uri in ontology_namespaces:
    #print(f"Prefix: {prefix}, URI: {uri}")


ontology_namespaces = get_ontology_namespace(graph)
#print(ontology_namespaces)


#json_ld = get_jsonLD(graph)

#print (json_ld)

class Matcher:
    def __init__(self, classes):
        self.classes = classes
    def match_class(self, feature):
        for obj in self.classes.triples((None, RDFS.label, Literal(feature))):
            return obj



m = Matcher(classes)
class_uri = m.match_class("Sensor")
assert "?" == class_uri, class_uri
    

#converted_data = Graph()
#with open('cit_a_pip.cvs') as f:
#    tablename = "??"
#    id, uid, zone, use_type, installed, material, joint, lining, diameter, d_cat, length_m = next(f)
#    candidate_uri = matcher.match_class(tablename, zone, material, joint, lining)
#    o = { '@id': uid,
#         '@type': candidate_uri,
#         '@context': 'http://mystuff',
#         'material', material,
#         # etc
#         }
#    converted_data.add(str(o))
    
