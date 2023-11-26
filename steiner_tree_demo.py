import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from networkx.algorithms.approximation import steiner_tree

similarity_index = 0.8

# Load CSV files into pandas DataFrames
users_df = pd.read_csv('data/users.csv')
products_df = pd.read_csv('data/products.csv')
orders_df = pd.read_csv('data/orders.csv')
order_details_df = pd.read_csv('data/order_details.csv')
addresses_df = pd.read_csv('data/addresses.csv')

# Add DataFrames to a dictionary for easy iteration
dfs = {
    'users': users_df,
    'products': products_df,
    'orders': orders_df,
    'order_details': order_details_df,
    'addresses': addresses_df
}

# Create a graph
G = nx.Graph()

# Function to calculate the Jaccard Index
def calculate_jaccard_index(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def add_graph_items(table_name, df):
    # Add nodes to the graph for each column
    columns = df.columns
    for col in columns:
        G.add_node(f"{table_name}.{col}", records=set(df[col].dropna()), table=table_name)

    # Connect each column to every other column within the same table
    for col1, col2 in combinations(columns, 2):
        G.add_edge(f"{table_name}.{col1}", f"{table_name}.{col2}")
        # You need to define how you calculate the similarity between col1 and col2 here

# Add items to graph
for table_name, df in dfs.items():
    add_graph_items(table_name, df)

# Custom function to calculate Jaccard index based on records attribute
def calculate_jaccard(G, node1, node2):
    records1 = G.nodes[node1]['records']
    records2 = G.nodes[node2]['records']
    intersection = len(records1.intersection(records2))
    union = len(records1.union(records2))
    return intersection / union if union != 0 else 0

# Add inter-table relationships based on column name and connect them
def add_inter_table_relationships(graph, dataframes):
    for table1, df1 in dataframes.items():
        for table2, df2 in dataframes.items():
            if table1 != table2:
                common_columns = set(df1.columns).intersection(df2.columns)
                for col in common_columns:
                    graph.add_edge(f"{table1}.{col}", f"{table2}.{col}")
                               
add_inter_table_relationships(G, dfs)

# Iterate over all combinations of nodes to calculate Jaccard index
for node1, node2 in combinations(G.nodes(), 2):
    jaccard_index = calculate_jaccard(G, node1, node2)
    if jaccard_index > similarity_index:
        # Add an edge for Jaccard index above 0.5
        G.add_edge(node1, node2, weight=jaccard_index)

# Print the edges with Jaccard index above 0.5
print("Jaccard Index Edges Added:")
for u, v, weight in G.edges(data='weight'):
    if weight is not None and weight > similarity_index:
        print(f"({u}, {v}) -> {weight:.8f}")

print("Graph created successfully!")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())
print("Graph Edges:")
print(G.edges())

# Define terminal nodes - modify this based on your requirements
start_nodes = {'users.email'}
target_nodes = {'order_details.product_id'}
terminal_nodes = start_nodes | target_nodes
# Compute the Steiner Tree
st_tree = steiner_tree(G, terminal_nodes, method='mehlhorn')

# Draw the original graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=700)
nx.draw_networkx_edges(G, pos, edgelist=G.edges())
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

# Highlight the edges of the Steiner Tree
nx.draw_networkx_edges(
    G, pos, edgelist=st_tree.edges(), width=3, alpha=0.5, edge_color="r"
) 

title_string_start = ', '.join(start_nodes)
title_string_target =  ', '.join(target_nodes)
title_string = "Network Steiner Tree: " + title_string_start + " to " + title_string_target + " (Red Edges)"

plt.title(title_string)
plt.axis("off")
plt.show()
