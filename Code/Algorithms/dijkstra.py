#!/usr/bin/env python
"""
Dijkstra's shortest path algorithm. 

Code from user Ionit Ticus via https://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python.
"""

class Dijkstra:

    def __init__(self, vertices, graph):
        self.vertices = vertices  # ("A", "B", "C" ...)
        self.graph = graph  # {"A": {"B": 1}, "B": {"A": 3, "C": 5} ...}

    def find_route(self, start, end):
        unvisited = {n: float("inf") for n in self.vertices}
        unvisited[start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbour, _ in self.graph.get(min_vertex, {}).items():
                if neighbour in visited:
                    continue
                new_distance = int(unvisited[min_vertex]) + int(self.graph[min_vertex].get(neighbour, float("inf")))
                if new_distance < unvisited[neighbour]:
                    unvisited[neighbour] = new_distance
                    parents[neighbour] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == end:
                break
        return parents, visited

    @staticmethod
    def generate_path(parents, start, end):
        path = [end]
        while True:
            key = parents[path[0]]
            path.insert(0, key)
            if key == start:
                break
        return path
    
    def get_results(vertices, graph, start, end):
        dijkstra = Dijkstra(vertices, graph)
        p, v = dijkstra.find_route(start, end)
        #print("START", start, end)
        #print(p,v)
        #print("Distance from %s to %s is: %.2f" % (start, end, v[end]))
        se = dijkstra.generate_path(p, start, end)
        #print("Path from %s to %s is: %s" % (start, end, " -> ".join(se)))
        return v[end], se