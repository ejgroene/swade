from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
import parser
import json
import pandas as pd
import os
#from langchain_core.runnables import RunnablePassthrough

output_parser = StrOutputParser()
llm = ChatOpenAI(openai_api_key="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", model_name="gpt-4-1106-preview", temperature=0)

#llm = ChatOpenAI(openai_api_key="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", model_name="gpt-3.5-turbo-1106", temperature=0)



base_filepath = "/Users/malikluti/Documents/MyProjects/SWADE/SWADE_Project/Data_Samples"

csv_filename = 'city_A.csv'

csv_content = pd.read_csv(os.path.join(base_filepath, csv_filename))

def get_column_names(pandas_input):
    return pandas_input.columns.tolist()

city_a_column_names = get_column_names(csv_content)

class_classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class classifier that finds the best matches between class properties"),
    ("user", "{input}")
])

class_classification_chain = class_classification_prompt | llm | output_parser

chunk_classes = []
champion_list = [] # [{name: Pipe, properties}, {name: Distribution etc.}]

chunk_classes = [parser.classes[x:x + 10] for x in range(0, len(parser.classes), 10)]
chunk_class_champion_names = [] # "Pipe", "DistributionPipe"

# record_no,syszone,use_type,inst_date,material,joint,joint_type,cathodic,diameter,length_ft

for chunk_classes_item in chunk_classes:
    chunk_output = class_classification_chain.invoke({"input": """

    Identify which of the Classes is the one that has most of the properties in common with the "properties" field with the list of comma separated properties: 

    List of comma separated properties:
    {comma_separated_properties} 

    Classes:
    {classes}


    The output needs to be only one word representing the class name matching with the "name" property of the Class object.
    
    If you do not find a proper class, just answer with N/A

    For example, if the matching class is 'River', the output needs to be only the word 'River'.


    Single word class name:
    """.format(classes=json.dumps(chunk_classes_item), comma_separated_properties=", ".join(get_column_names(csv_content)))})

    if chunk_output != "N/A":
        chunk_class_champion_names.append(chunk_output)

for champion_class_name in chunk_class_champion_names:
    for class_item in parser.classes:

        if class_item["name"] == champion_class_name:
            champion_list.append(class_item)
            break

estimated_class_name = class_classification_chain.invoke({"input": """

Identify which of the Classes is the one that has most of the properties in common with the "properties" field with the list of comma separated properties: 

List of comma separated properties:
{comma_separated_properties} 

Classes:
{classes}


The output needs to be only one word representing the class name matching with the "name" property of the Class object.

If you do not find a proper class, just answer with N/A

For example, if the matching class is 'River', the output needs to be only the word 'River'.


Single word class name:
""".format(classes=json.dumps(champion_list), comma_separated_properties=", ".join(get_column_names(csv_content)))})

print(estimated_class_name)

# Here we find the actual onthology class instance by classname
estimated_class = None

for class_item in parser.classes:
    if class_item["name"] == estimated_class_name:
        estimated_class = class_item
        break

assert estimated_class is not None

"""
1st iterations: class Pipe
2nd iteration: class Energy
3rd iteration: class Water
    
Which of these classes is the one that matches the most: 
1st iterations: class Pipe
2nd iteration: class Energy
3rd iteration: class Water
    
Pipe
"""

"""
Provided a list of csv columns AND provided a list of 100 onthology classes

1 - make 10 chunks of 10 onthology classes (10x10 = 100)
2 - iterate over each chunk by passing the csv columns and see which class is the winner in that chunk
3 - at this stage there will be 10 championList (one winner for each onthology chunk of 10 classes)
4 - make an llm call that contains only the winner classes to see who is the real winner
5 - create a 1:1 map between the columns names from the csv and the property name of the onthology class ("length" from csv - "Length of whatever" from the class)
5a - Mix the dataProperties and the objectProperties together in order to find the 1:1 match
5b - Split the dataProperties and objectProperties so that the actual values are mapped correctly in their original location 
(we need to generate a new dataProperties and a new objectProperties arrays filled with the data)
6 - Provided a subset of 5 rows from the CSV, generate a series of python scripts PLUS unit tests to transform the csv value into a standard Onthology value
e.g. generate a python script that turns "steel" from csv into "Steel" as specified in the onthology
"""
# TODO - EXTRACT THE LIST OF COLUMNS FOR EVERY CSV DATABASE AND CHANGE THE PROMPT ACCORDINGLY SO THAT IT'S PARAMETRIC

properties_matching_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

properties_matching_chain = properties_matching_prompt | llm | output_parser

chunk_output = properties_matching_chain.invoke({"input": """

Identify which of the Classes is the one that has most of the properties in common with the "properties" field with the list of comma separated properties: 

List of comma separated properties:
{comma_separated_properties}

Classes:
{classes}


The output needs to be only one word representing the class name matching with the "name" property of the Class object.

If you do not find a proper class, just answer with N/A

For example, if the matching class is 'River', the output needs to be only the word 'River'.


Single word class name:
""".format(classes=json.dumps(chunk_classes_item), comma_separated_properties=", ".join(get_column_names(csv_content)))})

"""
Now that we have the best estimated class.
We want to have another prompt that takes hte list of columns and the list of properties 
and generates a json 1:1 map between them

Here's what it looks like: 

{
CSV COLUMN - NAME OF PROPERTY FROM THE ONTHOLOGY CLASS
"length": "Length of whatever"
}
"""

# Creating the 1:1 match between the class property names and the csv columns

one_to_one_properties_matching_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are help assistant that can find the 1:1 match between class and property names"),
    ("user", "{input}")
])

one_to_one_properties_matching_chain = one_to_one_properties_matching_prompt | llm | output_parser

# Data Properties 1:1 Matches

one_to_one_property_matches_output_data_properties = one_to_one_properties_matching_chain.invoke({"input": """

Generate a JSON object containing a one to one association between the following two list of properties by matching the most similar ones semantically.

First list of properties:
{comma_separated_properties} 

Second list of properties
{onthology_class_comma_separated_properties}

The output needs to be a JSON object containing the second list of properties as keys and the matching first list of properties as values.

For example, if the best match for "hasCathodic" from the second list is "cathodic" from the first list, 
the JSON object will contain the following key/value: "hasCathodic" : "cathodic"  

For example, if the best for "hasDiameter" from the second list of properties is "diameter" from the first list of properties,
the jSON object will contain the following key/value: "hasDiameter":"diameter"

If you do not find a proper class, just answer with N/A

Here's an example of the output: {{"property":"value","second_property":"second_value"}}

The output should contain only json parsable characters. Avoid newline, spaces, and any other non-json symbol.

1 to 1 JSON Output:
""".format(
    comma_separated_properties=", ".join(get_column_names(csv_content)),
    onthology_class_comma_separated_properties=", ".join([property["name"] for property in estimated_class["dataProperties"]]))})

# 1:1 Object Properties Matches

one_to_one_property_matches_output_object_properties = one_to_one_properties_matching_chain.invoke({"input": """

Generate a JSON object containing a one to one association between the following two list of properties by matching the most similar ones semantically.

First list of properties:
{comma_separated_properties} 

Second list of properties
{onthology_class_comma_separated_properties}

The output needs to be a JSON object containing the second list of properties as keys and the matching first list of properties as values.

For example, if the best match for "hasCathodic" from the second list is "cathodic" from the first list, 
the JSON object will contain the following key/value: "hasCathodic" : "cathodic"  

For example, if the best for "hasDiameter" from the second list of properties is "diameter" from the first list of properties,
the jSON object will contain the following key/value: "hasDiameter":"diameter"

If you do not find a proper class, just answer with N/A

Here's an example of the output: {{"property":"value","second_property":"second_value"}}

The output should contain only json parsable characters. Avoid newline, spaces, and any other non-json symbol.

1 to 1 JSON Output:
""".format(
    comma_separated_properties=", ".join(get_column_names(csv_content)),
    onthology_class_comma_separated_properties=", ".join([property["name"] for property in estimated_class["objectProperties"]]))})

print("Data Properties")
print(json.loads(one_to_one_property_matches_output_data_properties))
print("Object Properties")
print(json.loads(one_to_one_property_matches_output_object_properties))

"""
{
    ONTHOLOGY         CSV
    "hasMaterial": "material",
    "hasJoint":  "joint"
}

CSV_A
{
    "steel": "Steel"
}
"""

# This is what we are going to ask the llm to do:
#we have material "steel" from csv and we have material "Steel" from onthology, generate a python function to turn "steel" into "Steel"
# def csv_to_onthology_value_convertr(csv_value):
#     whatever
#     return onthology_value
#^^^ will be saved into the onthology

#- Why are we mapping the csv columns names with the ontholoty names?
#- Why don't we care about the difference between the dataProperties and the objectProperties?' \ -> semantic similarity (e.g. is "hasJointType" more similar to "joint_type" or "cathodic")
#- What could we do with the property names match obtained in the 1:1 JSON object