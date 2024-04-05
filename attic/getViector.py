import os
import csv
from tkinter import ON
import parser
import torch
import numpy as np
import pandas as pd
import networkx as nx
from ast import Return
from sentence_transformers import SentenceTransformer, util

directory_path = r'C:\Users\gg363d\Source\Repos\swade\data'

def get_list_csv_filenames_without_extension(directory):
    
    """
    Get a list of all .csv file names (without extension) in the specified directory.
    
    Parameters:
    directory (str): The directory path.
    
    Returns:
    list: A list of .csv file names (without extension) in the directory.
    """
    csv_filenames_without_extension = []
    # List all files and directories in the specified directory
    for file in os.listdir(directory):
        # Check if the file ends with '.csv'
        if file.endswith('.csv'):
            # Remove the '.csv' extension and append the file name to the list
            csv_filenames_without_extension.append(file[:-4])
            
    return csv_filenames_without_extension


def get_tables_and_columns_names(directory_path, table_names):
    column_names_per_table = {}
    
    for table_name in table_names:
        file_path = os.path.join(directory_path, table_name + '.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            column_names_per_table[table_name] = df.columns.tolist()
    
    return column_names_per_table

def get_tables_and_columns_names_vectors():
    return
  
def get_ontology_class_names():
    
    ontology_class_names = []
    for i in parser.classes:
        ontology_class_names.append(i['name'])
        
    return ontology_class_names


def get_ontology_dataProperties():
    
    ontology_dataProperties = []
    for i in parser.classes:
        ontology_dataProperties.append(i['dataProperties'])
        
    print(ontology_dataProperties)    
    return ontology_dataProperties


def get_embeddings (names_list):
     
     model = SentenceTransformer("all-MiniLM-L6-v2")
     viectors = model.encode(names_list)
      
     return viectors


def get_cosign_similarity(list1, list2, list1_vector, list2_vector):
    
    #print (list1, list2)
    two_strings_and_cos_score = []
    
    cos_sim = util.cos_sim (list1_vector, list2_vector)
    
    for i in range(cos_sim.shape[0]):
        for j in range(cos_sim.shape[1]):
            #print ("The cosine similarity between the table name  ", list1[i], "", "and the ontology class is ", list2[j], " equal to  : " ,cos_sim[i][j])
            #This line will give a list of two strings and their cosine tensor value.
            #two_strings_and_cos_score.append([list1[i], list2[j], cos_sim[i][j]])
            #This is to convert the cosine tensor to a numerical value.
            two_strings_and_cos_score.append([list1[i], list2[j], float("{:.5f}".format(cos_sim[i][j]))])
          
    print (two_strings_and_cos_score)
    
    return two_strings_and_cos_score
 

def get_maximum_cosign_similarity(list1, list2, list1_vector, list2_vector):
    
    #print (list1, list2)
    two_strings_and_cos_score = []
    
    cos_sim = util.cos_sim (list1_vector, list2_vector)
    
    maxids = torch.argmax(cos_sim, dim=1).detach().numpy()
    scores = np.max(cos_sim.detach().numpy(), axis=1)
    #print("the id is :", maxids)
    pairs = list(zip(list1, np.array(list2)[maxids], scores))
    
    print(pairs)
    
    #breakpoint()
    
    return pairs  


#This is for testing:

# csv_filenames_list_without_extension = get_list_csv_filenames_without_extension(directory_path)
# csv_filenames_list_without_extension_viectors = get_embeddings(csv_filenames_list_without_extension)
 
# get_ontology_class_names = get_ontology_class_names()
 
# ontology_class_names_viectors = get_embeddings(get_ontology_class_names)

# testlist =[]
# testlist= get_maximum_cosign_similarity(csv_filenames_list_without_extension, get_ontology_class_names, csv_filenames_list_without_extension_viectors, ontology_class_names_viectors )

# #print(testlist)

# testlist2 =[]
# testlist2= get_cosign_similarity(csv_filenames_list_without_extension, get_ontology_class_names, csv_filenames_list_without_extension_viectors, ontology_class_names_viectors )

# #(testlist2)
# dat_Properties = []
# dat_Properties = get_ontology_dataProperties()
# dat_Properties_Viector = []
# for i in dat_Properties:
#     dat_Properties_Viector.append( get_embeddings(i))
#     print (i)

# mylist = []
# mylist = get_list_csv_filenames_without_extension(directory_path)

table_column_names_dictionary = get_tables_and_columns_names(directory_path, get_list_csv_filenames_without_extension(directory_path))
table_names =[]
table_names_viectors = []
column_names = []
column_names_viectors = []

# Print column names for each file
for table, columns in table_column_names_dictionary.items():
    #print(f"Columns in {table}: {columns}")
    table_names.append(table)
    table_names_viectors.append(get_embeddings(table))
    column_names.append(columns)

    column_names_viectors.append(get_embeddings(columns))
    
    #table_names_viectors.append(get_embeddings(table))

    #column_names.append(columns)
    #cloumn_viectors.append(get)
    
#print("The list of table names is   :", table_names_viectors)
#print("The list of column name victors is   :", column_names_viectors)
#print("The list of the table embeddings are  :", table_names_viectors )
print ("column size", len(column_names_viectors))

cosi=[]

cosi.append(get_maximum_cosign_similarity(column_names[0],column_names[1], column_names_viectors[0], column_names_viectors[1]))
print(cosi)

