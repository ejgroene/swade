# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 13:08:29 2021

@author: gg363d
"""
import pymongo
from pymongo import MongoClient
from SPARQLWrapper import SPARQLWrapper, JSON

url_read="http://54.177.164.145:3030/SwadeSaref/sparql"
url_write = "http://54.177.164.145:3030/SwadeSaref/update"
sparql_read = SPARQLWrapper(url_read)
sparql_write = SPARQLWrapper(url_write)


# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://smartuser:City2022@cluster0.bii1t.mongodb.net/smartcity?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client['smartcity']

coll = db['mqttmessages']

#records = db.mqttmessages.find({"topic": "Alamitos Reservoir"}).limit(5)

#for record in records:
#   print (record)
# print(records)


def data_retrieval(db, topic):
    records = db.mqttmessages.find({"topic": topic }).limit(5)

    print(records)
    fieldsLookUp = {
        # "pH": {"name": "HydrogenIonConcentration", "unit": ""},
        "turb": {"name": "Turbidity", "unit": "NTU"},
        # "orp": "Oxidisability",
        # "chlorine":
        # "chloramine"
        #"do":
        #"ec":
        #"t": "Temperature"


    }

    for record in records:
        id = record['_id']
        print (id)
        print (record['payload']['pH'])
        timeStamp = record['payload']['ts']
        payloadID = record['payload']['id']
        siteName = record['payload']['sn']
        lat = record['payload']['lat']
        lon = record['payload']['lon']

        pHValue = record['payload']['pH']
        turb = record['payload']['turb']
        orp = record['payload']['orp']
        chlorine = record['payload']['chlorine']
        chloramine = record['payload']['chloramine']
        dissolvedOxygen = record['payload']['do']
        electroConductivity = record['payload']['ec']
        temperature = record['payload']['t']

        queryString = """ PREFIX saref: <https://saref.etsi.org/core/>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX swade: <http://www.swade-saref.org/ontology#>
                        PREFIX wq: <http://water-quality.org/>
                        PREFIX unit: <http://www.ontology-of-units-of-measure.org/resource/om-2/>


                        insert data 
                        {
                         """

        for field in fieldsLookUp:
            id = str(id)
            timeStamp = str(timeStamp)
            field_value = record["payload"][field]
            field_metadata = fieldsLookUp[field]
            field_ref = field_metadata["name"]
            unit = field_metadata["unit"]
            queryString += """wq:Measurement{}{} rdf:type swade:Measurement .
                         wq:Measurement{}{} saref:hasTimestamp \"{}\" .
                         wq:Measurement{}{} saref:hasValue \"{}\" .
                         wq:Measurement{}{} saref:relateToProperty saref:{} .
                         wq:Measurement{}{} saref:isMeasuredIn unit:{} .
                         """.format(
                         id, field, id, field, timeStamp, id, field, field_value, id, field, field_ref, id, field, unit)

        queryString += "}"

        print(queryString)

        sparql_write.setQuery(queryString)
        sparql_write.method = 'POST'
        sparql_write.query()


def main():
    client = MongoClient(CONNECTION_STRING)
    db = client['smartcity']
    # coll = db["mqttmessages"]
    data_retrieval(db, "Alamitos Reservoir")


if __name__ == "__main__":
    main()
#
# wq:Measurement"""+ str(id) + """ saref:turb """+ str(turb) + """ .
# wq:Measurement"""+ str(id) + """ saref:chlorine """+ str(chlorine) + """ .
# wq:Measurement"""+ str(id) + """ saref:orp """+ str(orp) + """ .
# wq:Measurement"""+ str(id) + """ saref:chloramine """+ str(chloramine) + """ .


# """ wq:Measurement"""+ str(id) + """pHValue rdf:type swade:Measurement .
#              wq:Measurement"""+ str(id) + """pHValue saref:hasTimestamp \""""+ str(timeStamp) + """\" .
#              wq:Measurement"""+ str(id) + """pHValue saref:hasValue \""""+ str(pHValue) + """\" .
#              wq:Measurement"""+ str(id) + """pHValue saref:relateToProperty saref:HydrogenIonConcentration .
#              wq:Measurement"""+ str(id) +"""turb rdf:type swade:Measurement .
#              wq:Measurement"""+ str(id) + """turb saref:hasTimestamp \""""+ str(timeStamp) + """\" .
#              wq:Measurement"""+ str(id) + """turb saref:hasValue \""""+ str(turb) + """\" .
#              wq:Measurement"""+ str(id) + """turb saref:relateToProperty saref:Turbidity .