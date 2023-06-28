#!/usr/bin/env python 
"""
Class for the algorithm for the Route Inspection Problem/Postman Tour. Makes use of Dijkstra's shortest
path algorithm.
"""
import copy
from typing import Tuple, Any, Dict, List
from Code.Classes.station_postman import Station_Postman
from Code.Algorithms.dijkstra import Dijkstra

class Postman():
    """
    Station class representing a station, its location in coordinates, 
    if it has been visited, and its connections

    Attributes:
    - - - - - - - 
    - vertices: List[str]
        a list of station names that represent the vertices in the graph
    - graph
        the name of the station 
    - connections: Dict[str, Dict[str, int]]
        the other stations that the station is connected to, 
        and how long the travel time is
    """
    def __init__(self, vertices: List[str], graph: Dict) -> None:
        self.vertices: List[str] = vertices 
        self.graph: Dict = graph # {"A": {"B": 1}, "B": {"A": 3, "C": 5} ...}

    def odd_vertices(self) -> List[str]:
        """
        Returns all the vertices with an odd degree of edges.
        By the Handshaking theorem, there are always an even number of odd vertices.
        """
        odd = []
        for vertex in self.vertices:

            # If the number of connections is not even, vertex has odd degree
            if len(list(self.graph[vertex])) % 2 != 0: 
                odd.append(vertex)
        
        return odd

    def possible_pairs(odd: List[str]) -> List[List[Tuple[str, str]]]:
        """
        Returns all the possible combinations of pairs. The graph is undirected so (a, b) == (b, a), meaning
        a fewer pairs than for a directed graph. 
        
        Pairs are selected by going down the list of vertices, so 
        (a, b), (a, c)), ..., (b, c), (b, d), ..., (c, d), (d, e), etc.
        """
        possible_pairs = []
        for vertex in odd:
            combination = []
            for i in range(odd.index(vertex) + 1, len(odd)):

                # Ensures no pairs of form (a, a), (b, b), ...
                if vertex != odd[i]:
                    combination.append((vertex, odd[i]))
            if len(combination) > 0:
                possible_pairs.append(combination)
        return possible_pairs

    def shortest_pair_path(self, possible_pairs: List[List[Tuple[str, str]]]) -> Dict:
        """
        Calculates the shortest paths for all possible pairs using Dijkstra's shortest path algorithm.
        For every list of pairs, the total weight of the pairings is calculated. The list with the minimum
        weight is chosen.

        Returns them in a dictionary of form paths[(start_vertex, end_vertex)] = {(weight_of_shortest_path, route_taken)}.
        """
        paths: Dict = {}
        total_sums = []

        # Lisingt is the list of [(a, b), (c, d), ...] pairs
        for listing in possible_pairs: 
            sum_pairs = 0
            for pair in listing:
                # Weight of shortest path
                distance, route = Dijkstra.get_results(self.vertices, self.graph, pair[0], pair[1])
                sum_pairs += distance
            total_sums.append(total_sums)

        min_index = total_sums.index(min(total_sums))
        pairings = possible_pairs[min_index]
        for pair in pairings:
                
                # Weight of shortest path
                distance, route = Dijkstra.get_results(self.vertices, self.graph, pair[0], pair[1])
                paths[(pair[0], pair[1])] = (distance, route)
        
        return paths
    

    def find_min(self, weights: List[int], pairs: List[Any]) -> Tuple[str, str]:
        """
        Finds the minimum weight of an edge and returns between which vertices this minimum occurs.
        """
        # Find the minimum of all paths for that particular start vertex
        if weights:  
            minimum = min(weights)
            index_min = weights.index(minimum)
            start_v, end_v = pairs[index_min]

        return start_v, end_v
    
    def remove_stations(self, keys: List[str], start_v: str, end_v: str) -> List[str]:
        """
        Removes the stations from the list of possible pairs if they've already been used.
        """
        to_remove = []
        for tpl in keys:
            if tpl[0] == start_v or tpl[0] == end_v or tpl[1] == start_v or tpl[1] == end_v:
                to_remove.append(tpl)

        for tu in to_remove:
            keys.remove(tu)

        return keys

    def minimum_matching(self, paths: Dict) -> List[Tuple[str, str, int]]:
        """
        Finds the minimum matching of the shortest paths between uneven vertices. Returns a 
        list of the connections and their weight. 
    
        """
        keys = list(paths.keys())  # List of all the start vertices
        shortest_paths = []

        while keys:
            start = keys[0][0]
            starters = [tpl for tpl in keys if tpl[0] == start] # List of all pairs with the same start_vertex
            weights = []

            # paths[(start, end)] = [list of vertex connections of form (distance, route), ...]
            for pair in starters:  
                distance, route = paths[pair]
                weights.append(distance)

            # Finds the pair with the minimum shortest path starting from that starting vertex
            start_v, end_v = self.find_min(weights, starters)
            shortest_paths.append((start_v, end_v, distance))

            # Removes all pairs with the same start_vertex and end_vertex from possible paths
            keys = self.remove_stations(keys, start_v, end_v) 

        return shortest_paths

    def add_edge(self, modified_graph: Dict, start: str, end: str, edge: str) -> Dict:
        """
        Determines if the new edge is less than the existing edge.

        Returns the graph with the new edge.
        """
        if edge > modified_graph[start][end]:
            modified_graph[start][end] = [modified_graph[start][end], modified_graph[start][end]]
            modified_graph[end][start] = [modified_graph[end][start], modified_graph[end][start]]
        else: 
            modified_graph[start][end] = [modified_graph[start][end], edge]
            modified_graph[end][start] = [modified_graph[end][start], edge]

        return modified_graph    

    def modify_graph(self, shortest_paths: List[Tuple[str, str, int]]) -> Dict:
        """
        Adds edges from the minimum matching function to the graph. Returns the modified graph.
        
        shortest_paths is a list of form [(start_vertex, end_vertex, weight, route), etc.]
        """
        modified_graph = copy.deepcopy(self.graph)
        # path is a tuple of form (a, b, c)
        for path in shortest_paths: 
            start = path[0]
            end = path[1]
            edge = path[2]

            # If there is already a connection from the start to end vertex, a list of the routes is created
            if end in list(modified_graph[start].keys()): 
                modified_graph = self.add_edge(modified_graph, start, end, edge)

            else:
                modified_graph[start][end] = edge
                modified_graph[end][start] = edge

        return modified_graph
    
    def check_type(self, obj: Any) -> bool:
        """
        Returns True if the object is a list.

        Returns False otherwise.
        """
        if isinstance(obj, list):
            return True
        else:
            return False
        
    def check_bridge(self, graph: Dict, connection: str) -> bool:
        """
        Checks if a connection is a bridge, i.e., it has a singular connection
        that has no way back if used.
        """
        if graph[connection].keys() == 1:
            return True
        else:
            return False
        
    def get_non_bridges(self, graph: Dict, possible_connections: List[str]) -> List[str]:
        """
        Returns a list of all the connections that are not bridges, i.e., connections with only
        one edge.

        If only bridges exist, returns list of bridges.
        """
        non_bridges = []

        for connection in possible_connections: # Checks if there are connections that are not bridges 
            if self.check_bridge(graph, connection) is False:
                non_bridges.append(connection)

         # If the only options are bridges
        if len(non_bridges) < 1:
            non_bridges = possible_connections
            
        return non_bridges
        
    def get_possible_edges(self, graph: Dict, current_vertex:str, non_bridges: List[str]) -> List[int]:
        """
        Returns list of weights of possible connections.
        """
        possible_edges = [] 

        # Minimum edge is selected, and its weight is added to the sum of the circuit
        # List of possible edges to traverse from current_vertex
        for key in non_bridges:  
            edge = graph[current_vertex][key]

            # If there are multiple routes for the same pair, finds the minimum
            if self.check_type(edge) is True: 
                edge = [int(num) for num in edge]
                connection = int(min(edge))
            else:
                connection = int(edge)
            possible_edges.append(connection)
        
        return possible_edges

    def all_visited(self) -> bool:
        """
        Returns True if all connections have been visited.
        """
        keys = list(self.graph.keys())
        unvisited = 0
        for key in keys:
            if len(self.graph[key]) > 0:
                unvisited += 1

        if unvisited == 0:
            return True
        else:
            return False
    
    def del_connection(self, current_vertex: str, possible_connections: List[str], min_index: int) -> None:
        """
        Deletes connection in (original) graph so that it can be determined if all
        connections have been visited.
        """
        if self.graph[current_vertex] and possible_connections[min_index] in list(self.graph[current_vertex].keys()):
            del self.graph[current_vertex][possible_connections[min_index]]
            del self.graph[possible_connections[min_index]][current_vertex]

    def new_trajectory(self, trajectories: List[List[str]], total_weight: int) -> Tuple[List[List[str]], int]:
        """
        Adds the trajectory to the list of trajectories and resets the weight to 0.

        Returns the updated list of trajectories and weight.
        """
        if trajectories:
            length = len(self.stack) - len(trajectories[0][-1])
            route = self.stack[:-(length+1):-1]
        else:
            route = self.stack[::-1]
            
        trajectories.append((total_weight, route))
        total_weight = 0

        return trajectories, total_weight

    def walking(self, graph: Dict, total_weight: int, trajectories: List[Tuple[Any, Any]], max_time: int) -> Tuple[Dict, int, List[Tuple[Any, Any]]]:
        """
        Recursive function from step 2 of the algorithm. Returns the circuit of the 
        Euler path and the total weight of the circuit.
        """
        self.stack.append(self.current_vertex)

        # All possible connections from the current vertex
        possible_connections = list(graph[self.current_vertex].keys())
        non_bridges = self.get_non_bridges(graph, possible_connections)

        # Get list of possible edges
        possible_edges = self.get_possible_edges(graph, self.current_vertex, non_bridges)
        
        minimum = min(possible_edges) # If there are multiple connections, finds the minimum
        min_index = possible_edges.index(minimum)

        if (total_weight + int(minimum)) > max_time:
            trajectories, total_weight = self.new_trajectory(trajectories, total_weight)
        
        # Adds to the total weight of the circuit
        total_weight += int(minimum)  

        # Removes connection as it has been used
        possible_edges.remove(minimum) 

        # Removes connection from modified graph
        del graph[self.current_vertex][possible_connections[min_index]] 

        # Removes connection from original graph
        self.del_connection(self.current_vertex, possible_connections, min_index) 

        # Neighbouring vertex assigned as the new current vertex
        self.current_vertex = possible_connections[min_index]

        # If current vertex still has connections to its neighbour(s), process continues to run
        while len(graph[self.current_vertex]) > 0 and len(self.stack) > 0 and (self.all_visited() == False):
            graph, total_weight, trajectories = self.walking(graph, total_weight, trajectories, max_time)
            if len(graph[self.current_vertex]) == 0:
                self.circuit.append(self.current_vertex)
                self.current_vertex = self.stack.pop()

        return graph, total_weight, trajectories
        
    def euler_path(self, modified_graph: Dict, start_vertex: str, max_time: int) -> Tuple[List[str], List[Tuple[str, int]]]:
        """
        Algorithm for finding a Euler path in a graph. Returns the circuit.

        From http://www.graph-magics.com/articles/euler.php: 
        1. Start with an empty stack and an empty circuit (eulerian path).
        2. If current vertex has no neighbors - add it to circuit, remove the last vertex 
            from the stack and set it as the current one. Otherwise (in case it has neighbors) - 
            add the vertex to the stack, take any of its neighbors, remove the edge between 
            selected neighbor and that vertex, and set that neighbor as the current vertex.
        3. Repeat step 2 until the current vertex has no more neighbors and the stack is empty.
        """
        self.stack: List[str] = []
        total_weight = 0
        self.circuit: List[str] = []
        self.current_vertex = start_vertex
        trajectories: List[Tuple[str, int]] = []
        modified_graph, total_weight, trajectories = self.walking(modified_graph, total_weight, trajectories, max_time)

        return self.circuit, trajectories
    
    