import selftest
test = selftest.get_tester(__name__)

import owlready2
import pathlib
import rdflib

testdatadir = pathlib.Path(__file__).parent.parent/'data'

@test
def read_ontology():
    n3_filename = testdatadir/"swade.n3"
    graph = rdflib.Graph()
    for f in testdatadir.glob('*.ttl'):
        graph.parse(f)
    graph.serialize(destination=n3_filename.as_posix(), format="ntriples")

    p = "file://" + n3_filename.as_posix()
    print(">>>", p)
    o = owlready2.get_ontology(p)
    classes = o.classes()
    test.eq('?', list(classes))