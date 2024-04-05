from huggingface_hub.utils import get_aiohttp_version
import getViector
import networkx as nx
import matplotlib.pyplot as plt

import parser

def generate_bipartite_matching(data_list):
    """
    Create a bipartite graph and generate the maximum bipartite matching from the given data.

    Parameters:
    data_list (list): List of elements. Each element consists of two strings and their similarity score.

    Returns:
    matching (dict): Dictionary representing the maximum matching.
                     Keys are nodes from the first partition,
                     values are the corresponding matched nodes from the second partition.
    """
    # Create an empty bipartite graph
    bipartite_graph = nx.Graph()
    print("the graph is   :", bipartite_graph)
    # Add nodes from the first partition (strings)
    bipartite_graph.add_nodes_from([element[0] for element in data_list], bipartite=0)
    bipartite_graph.add_nodes_from([element[1] for element in data_list], bipartite=1)
    
    # Step 2: Add edges between nodes of different sets with weights
    # edges = [(1, 'a', 10), (1, 'b', 5), (2, 'b', 7), (3, 'c', 10), (4, 'a', 1)]
    # Each edge is a tuple (node1, node2, weight)
    bipartite_graph.add_weighted_edges_from(data_list)
    
    #print("the graph is   :", bipartite_graph)

    # Find the maximum bipartite matching
    #matching = nx.bipartite.weight_matching(bipartite_graph)
    matching = nx.max_weight_matching(bipartite_graph)
    #print(matching)
    
    # Separate the nodes by their bipartite attribute for visualization
    top_nodes = {n for n, d in bipartite_graph.nodes(data=True) if d['bipartite'] == 0}
    bottom_nodes = set(bipartite_graph) - top_nodes
    
    #print ("the top nodes are  :", top_nodes)
    #print ("the bottom_nodes are  :", bottom_nodes)

    # Draw the bipartite graph
    pos= nx.bipartite_layout(bipartite_graph, top_nodes)
    nx.draw(bipartite_graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=12, font_weight='bold')

    # Add edge labels
    edge_labels = nx.get_edge_attributes(bipartite_graph, 'weight')
    nx.draw_networkx_edge_labels(bipartite_graph, pos, edge_labels=edge_labels)

    plt.title("Weighted Bipartite Graph")
    plt.show()

    return matching


directory_path = r'C:\Users\gg363d\Source\Repos\swade\data'

table_names = []
table_names_viectors = []

class_names = []
class_names_viectors = []
table_class_names_cos_score = []

table_names = getViector.get_list_csv_filenames_without_extension(directory_path)
table_names_viectors = getViector.get_embeddings(table_names)
class_names = getViector.get_ontology_class_names()
 
class_names_viectors = getViector.get_embeddings(class_names)

table_class_names_cos_score = getViector.get_cosign_similarity(table_names, class_names, table_names_viectors, class_names_viectors)



# Generate the maximum bipartite matching
matching = generate_bipartite_matching(table_class_names_cos_score)


dataProperties = getViector.get_ontology_dataProperties()
dataProperties_viectors = getViector.get_embeddings(dataProperties)


table_column_names_dictionary = getViector.get_tables_and_columns_names(directory_path, getViector.get_list_csv_filenames_without_extension(directory_path))



columns_list = []

# Print column names for each file
for table, columns in table_column_names_dictionary.items():
    columns_list.append(columns)
    #print(f"Columns in {table}: {columns}")
    
print ("The columns are .....", columns_list )

columns_list_viectors = getViector.get_embeddings(columns_list)
print (columns_list_viectors)

#TODO apply Levenshtein algorithm https://www.analyticsvidhya.com/blog/2021/07/fuzzy-string-matching-a-hands-on-guide/

