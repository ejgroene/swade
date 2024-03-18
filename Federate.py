from SPARQLWrapper import SPARQLWrapper, JSON

url_read="http://54.219.17.84:8080/sparql"
url_write = "http://54.219.17.84:8080/sparql"
sparql_read = SPARQLWrapper(url_read)
sparql_write = SPARQLWrapper(url_write)

# queryString = """

# PREFIX saref: <https://saref.etsi.org/core/>
# SELECT * WHERE {
#   {SERVICE <http://54.219.17.84:8080/sparql> {
#      ?s a saref:Measurement ; saref:hasValue ?value ; saref:hasTimestamp ?time .
#      FILTER(STR(?value) > "20")
#     } } UNION
#   {SERVICE <http://54.219.17.84:8081/sparql> {
#      ?s a saref:Measurement ; saref:hasValue ?value ; saref:hasTimestamp ?time .
#      FILTER(STR(?value) > " 20")
#     } }
# }
# """

queryString = """
PREFIX saref: <https://saref.etsi.org/core/>
SELECT * WHERE { 
  ?s a saref:Measurement ; ?p ?o ; saref:hasTimestamp ?time 
  FILTER( ?time > "1648412687" ) 
}
"""
sparql_read.setQuery(queryString)
resolved = sparql_read.queryAndConvert()
with open('op.xml', 'w') as writer:
    resolved.writexml(writer)
print(resolved.toprettyxml().find("swademesurement"))