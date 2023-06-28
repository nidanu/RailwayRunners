#!/usr/bin/env python # 
"""
Visualises train stop & their connections in a network map. 

The nodes are plotted using the coordinates of the stations as specified in 
the Station class.
"""
#import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import sys
from pyvis.network import Network
sys.path.append('..')
from Code.Classes.station import Station
from typing import Any, Type

def network_map(Station: Type['Station']) -> Any:
    """
    Visualises train stop & their connections in a network map. 

    The nodes are plotted using the coordinates of the stations as specified in 
    the Station class.
    """

    nodes = []
    edges = []
    for station in Station:
        keys = (list(station.connections.keys()))
        nodes.append((station.station_name, station.x, station.y))
        for key in keys:
            edges.append((station.station_name, key, station.connections[key]))

    # Create a new figure and axis
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Remove axis and tick marks
    ax.axis('off')

    # Draw nodes
    for i, node in enumerate(nodes):
        ax.scatter(nodes[i][1], nodes[i][2], marker='o', s=200, c='skyblue')
        ax.text(nodes[i][1], nodes[i][2], nodes[i][0], ha='center', va='center', fontsize=9, weight='bold')

    # Draw edges
    for edge in edges:
        start, end, weight = edge
        start_node = next((n for n in nodes if n[0] == start), None)
        end_node = next((n for n in nodes if n[0] == end), None)
        mid_x = (start_node[1] + end_node[1]) / 2
        mid_y = (start_node[2] + end_node[2]) / 2
        if start_node and end_node:
            ax.plot([start_node[1], end_node[1]], [start_node[2], end_node[2]], 'k-', linewidth=0.5)
            ax.text(mid_x, mid_y, weight, ha='center', va='center')

    # Display the graph
    plt.show()

def nx_network(Station: Type['Station']):
    G = nx.Graph()
    nodes = []
    edges = []
    for station in Station:
        keys = (list(station.connections.keys()))
        nodes.append((station.station_name, station.x, station.y))
        for key in keys:
            edges.append((station.station_name, key, station.connections[key]))
    pos = {}
    
    for node in nodes:
        G.add_node(node[0], size=15)
        pos[node[0]] = (node[1], node[2])
    for edge in edges:
        start_node = edge[0]
        end_number = int(edge[1])
        weight = int(edge[2])
        end_node = nodes[end_number][0]
        G.add_edge(start_node, end_node, weight=weight)

    net = Network(notebook=True)
    net.from_nx(G)
    net.write_html("../Visualisation/graph.html")
