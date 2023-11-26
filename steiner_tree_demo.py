import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from networkx.algorithms.approximation import steiner_tree

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

# Function to add columns of a DataFrame as nodes and connect them
def add_columns_as_nodes_and_connect(df, table_name, graph):
    columns = df.columns
    for col in columns:
        graph.add_node(f"{table_name}.{col}", table=table_name)
    # Connect each column to every other column within the same table
    for col1, col2 in combinations(columns, 2):
        graph.add_edge(f"{table_name}.{col1}", f"{table_name}.{col2}")

# Add columns of each table as nodes and connect them
add_columns_as_nodes_and_connect(users_df, 'users', G)
add_columns_as_nodes_and_connect(products_df, 'products', G)
add_columns_as_nodes_and_connect(orders_df, 'orders', G)
add_columns_as_nodes_and_connect(order_details_df, 'order_details', G)
add_columns_as_nodes_and_connect(addresses_df, 'addresses', G)

def add_inter_table_relationships(graph, dataframes):
    for table1, df1 in dataframes.items():
        for table2, df2 in dataframes.items():
            if table1 != table2:
                common_columns = set(df1.columns).intersection(df2.columns)
                for col in common_columns:
                    graph.add_edge(f"{table1}.{col}", f"{table2}.{col}")

add_inter_table_relationships(G, dfs)

print("Graph created successfully!")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# Define terminal nodes - modify this based on your requirements
start_nodes = {'users.email'}
target_nodes = {'order_details.product_id'}
terminal_nodes = start_nodes | target_nodes
# Compute the Steiner Tree
st_tree = steiner_tree(G, terminal_nodes)

# Draw the original graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=700)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1)
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
