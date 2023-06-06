#!/usr/bin/env python # 
"""
Visualises train stop & their connections
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# Load connections into Station objects
with open("ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(28):    
        connection = f.readline()
        connection = connection.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime = connection[2].split('\n')
        traveltime = int(traveltime[0])
        G.add_edge(station_1, station_2, weight=traveltime)

# Code from https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html#sphx-glr-auto-examples-drawing-plot-weighted-graph-py       


pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(G, pos, node_size=100)

# edges
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edges(
    G, pos, width=2, alpha=0.5, edge_color="black", style="solid"
)

# node labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()
