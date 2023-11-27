import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from networkx.algorithms.approximation import steiner_tree
from pyvis.network import Network

 # Set similarity index threshold for edge creation. Set to greater than 1 to disable. 
#similarity_index = 0.5

# Set terminal nodes to find path
#start_nodes = {'users.email'}
#target_nodes = {'order_details.product_id'} 

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

# Function to calculate the Jaccard Index
def calculate_jaccard_index(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def add_graph_items(G,table_name, df):
    # Add nodes to the graph for each column
    columns = df.columns
    for col in columns:
        G.add_node(f"{table_name}.{col}", records=set(df[col].dropna()), table=table_name)

    # Connect each column to every other column within the same table
    for col1, col2 in combinations(columns, 2):
        G.add_edge(f"{table_name}.{col1}", f"{table_name}.{col2}",weight=1,color='black')
        # You need to define how you calculate the similarity between col1 and col2 here

# Custom function to calculate Jaccard index based on records attribute
def calculate_jaccard(G, node1, node2):
    records1 = G.nodes[node1]['records']
    records2 = G.nodes[node2]['records']
    intersection = len(records1.intersection(records2))
    union = len(records1.union(records2))
    return intersection / union if union != 0 else 0

# Add inter-table relationships based on column name and connect them
def add_inter_table_relationships(G, dataframes):
    for table1, df1 in dataframes.items():
        for table2, df2 in dataframes.items():
            if table1 != table2:
                common_columns = set(df1.columns).intersection(df2.columns)
                for col in common_columns:
                    G.add_edge(f"{table1}.{col}", f"{table2}.{col}",weight=1,color='blue')

def auto_relation(similarity_index,start_nodes,target_nodes):
    # Create a graph
    G = nx.Graph()

    # Add base items to graph
    for table_name, df in dfs.items():
        add_graph_items(G,table_name, df)
        
    # Add inter-table relationships to graph                  
    add_inter_table_relationships(G, dfs)

    # Add Jaccard relations to graph - Iterate over all combinations of nodes to calculate Jaccard index
    for node1, node2 in combinations(G.nodes(), 2):
        jaccard_index = calculate_jaccard(G, node1, node2)
        if jaccard_index > similarity_index and not G.has_edge(node1, node2):
            # Add an edge for Jaccard index above similarity_index variable
            G.add_edge(node1, node2, weight=jaccard_index,color='yellow')
        
    """ 
    # Print the edges with Jaccard index above similarity_index variable
    print("Jaccard Index Edges Added:")
    for u, v, weight in G.edges(data='weight'):
        if weight is not None and weight > similarity_index:
            print(f"({u}, {v}) -> {weight:.8f}")

    print("Graph created successfully!")
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges()) 
    """
    
    start_nodes_split = start_nodes.split(',')
    target_nodes_split = target_nodes.split(',')

    terminal_nodes = start_nodes_split + target_nodes_split
    # Compute the Steiner Tree
    st_tree = steiner_tree(G, terminal_nodes, method='mehlhorn')

    main_edges = G.edges()
    main_edge_colors = [G[u][v]['color'] for u,v in main_edges]
    
    for u, v in st_tree.edges():
        if G.has_edge(u, v):
            G[u][v]['color'] = 'red'

    # Draw the main graph
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G, k=0.15, iterations=25)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=main_edge_colors)
    nx.draw_networkx_labels(G, pos)

    # Highlight the edges of the Steiner Tree
    nx.draw_networkx_edges(G, pos, edgelist=st_tree.edges())

    """
    title_string_start = ', '.join(start_nodes_split)
    title_string_target =  ', '.join(target_nodes_split)
    title_string = "Network Steiner Tree: " + title_string_start + " to " + title_string_target + '''
    Black = Intra-Table, Blue  = Inter-table, Yellow = Jaccard Relation, Red = Steiner Tree
    '''

    plt.title(title_string)
    plt.axis("off")
    """
    
    for node, data in G.nodes(data=True):
        for key, value in data.items():
            if isinstance(value, set):
                # Convert set to list
                G.nodes[node][key] = list(value)

    for u, v, data in G.edges(data=True):
        for key, value in data.items():
            if isinstance(value, set):
                # Convert set to list
                G[u][v][key] = list(value)
        
    net = Network(heading='')
    net.from_nx(G)  # Assuming S is your Steiner tree or the graph you want to visualize

    # Customize the network (optional, you can add more customization as needed)
    #net.show_buttons(filter_=['physics'])  # This line will show buttons to manipulate physics settings interactively

    # Save and show the network
    net.save_graph("front.html")
