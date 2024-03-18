
from SPARQLWrapper import SPARQLWrapper, JSON

url_carson = "http://54.177.230.233:8080/sparql"
url_anaheim = "http://54.177.230.233:8081/sparql"

endpoint_carson = SPARQLWrapper(url_carson)
endpoint_anaheim = SPARQLWrapper(url_anaheim)

endpoint_carson.setReturnFormat(JSON)
endpoint_anaheim.setReturnFormat(JSON)

queryString_1 = """
PREFIX no: <http://km.aifb.kit.edu/projects/numbers/number#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://www.semanticweb.org/malikluti/ontologies/swade#>
PREFIX saref: <https://saref.etsi.org/saref4watr/>

SELECT
?material (sum(?length) as ?length_sum) 
(sum(?length)*100/?totalLength as ?Percentage_Of_Network) WHERE {
  ?pipe 
        :hasMaterial ?material ;
        :hasLength ?length .

  {
    SELECT (sum(?length)/1 as ?totalLength) WHERE {
      ?pipe :hasLength ?length .
    }
  }  
}
group by ?material  ?totalLength
order by ?material  
"""
endpoint_carson.setQuery(queryString_1)

combined_results = []

try:
    ret = endpoint_carson.queryAndConvert()

    for r in ret["results"]["bindings"]:
        print(r)
        combined_results.append(r)
except Exception as e:
    print(e)

endpoint_anaheim.setQuery(queryString_1)
try:
    ret2 = endpoint_anaheim.queryAndConvert()

    for r in ret2["results"]["bindings"]:
        print(r)
        combined_results.append(r)
except Exception as e:
    print(e)


print("union")
print(len(combined_results))
print(combined_results)

