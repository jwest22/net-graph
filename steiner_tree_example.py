import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import steiner_tree

data = pd.read_csv("graphdata.csv")
# Create a DataFrame
df = pd.DataFrame(data)

# Initialize a graph
G = nx.Graph()

# Add edges to the graph
for index, row in df.iterrows():
    # Inverting 'relationship %' to define edge weight (optional)
    weight = 100 - row['Weight']
    G.add_edge(row['Source'], row['Target'], weight=weight)

# Define terminal nodes - modify this based on your requirements
start_nodes = {'col_1','col_2'}
target_nodes = {'col_19'}
terminal_nodes = start_nodes | target_nodes
# Compute the Steiner Tree
st_tree = steiner_tree(G, terminal_nodes)

# Draw the original graph
plt.figure(figsize=(15, 15))

pos = nx.spring_layout(G, k=0.15, iterations=20)  # positions for all nodes

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
