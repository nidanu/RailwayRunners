#!/usr/bin/env python # 
"""
Visualises train stop & their connections in a network map.
"""
import matplotlib.pyplot as plt

nodes = []
edges = []

# Count number of connections
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)   
    num_connections = len(f.readlines())

# Add all edges to list
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(num_connections):    
        connection = f.readline()
        connection = connection.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime = connection[2].split('\n')
        traveltime = int(traveltime[0])

        edges.append((station_1, station_2, traveltime))

# Count number of stations
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())

# Add all nodes and their coordinates into list
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)

    for i in range(num_stations):
        station_info = f.readline().split(',')
        station_info = station_info
        station_name = station_info[0]
        
        station_y = float(station_info[1])
        station_x_str = station_info[2].split('\n')
        station_x = float(station_x_str[0]) 
        nodes.append((station_name, station_x, station_y))
        
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
    if start_node and end_node:
        ax.plot([start_node[1], end_node[1]], [start_node[2], end_node[2]], 'k-', linewidth=0.5)

# Display the graph
plt.show()