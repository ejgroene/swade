from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


g = Graph()
g.parse("swade.ttl", format="ttl")
for subject, predicate, object in g:
    print(subject)

#print(g)

def a_function(o, d):
    pass

class MyTests(unitetst.TestCase):
    def test_my_first_test_assuption(self):
        o = g.parse("swade.ttl", format="ttl")
        self.equal("?", o)
        self.
        Y = a_function(o, {})


# queryString_0 = """
#
# SELECT * {
#   SERVICE <http://54.177.230.233:8081/sparql> {
#     {
#       SELECT ?s ?p ?o {
#         ?s ?p ?o
#       } LIMIT 10
#     }
#   }
# }
# """
# results = g.query(queryString_0)
# print(len(results))
# for row in results:
#     print(row)
x =list(
    g.query("""\
      SELECT *
        WHERE {
          SERVICE <http://54.177.230.233:8081/sparql> {
            {
              SELECT ?s ?p ?o
              WHERE {
                ?s ?p ?o
              }
              LIMIT 10
            }
          }
        }"""
    )
)
print(x)