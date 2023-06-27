#!/usr/bin/env python 
"""
Algorithm for the Route Inspection Problem/Postman Tour. Makes use of Dijkstra's shortest
path algorithm.
"""
import random
import copy
import sys
from statistics import mean
from typing import Tuple, Any, Dict, List, Union

sys.path.append("..")
from Classes.station_postman import *
from Algorithms.dijkstra import *

class Postman():
    """
    Class to tackle the Postman tour.
    """
    def __init__(self, vertices: list[str], graph: Dict) -> None:
        self.vertices: list[str] = vertices 
        self.graph: Dict = graph # {"A": {"B": 1}, "B": {"A": 3, "C": 5} ...}

    def odd_vertices(self) -> List[str]:
        """
        Returns all the vertices with an odd degree of edges.
        By the Handshaking theorem, there are always an even number of odd vertices.
        """
        odd = []
        for vertex in self.vertices:
            if len(list(self.graph[vertex])) % 2 != 0: # If the number of connections is not even, vertex has odd degree
                odd.append(vertex)
        return odd
    
    def selection_start(odd: List[str]) -> Tuple[str, str, List[str]]:
        """
        Randomly selects start and end vertices. The start vertex does not have to 
        equal the end vertex, thus the path is more efficient.
        """
        index_start = random.randint(0, len(odd) - 1)
        start_vertex = odd[index_start]

        del odd[index_start] # Removes vertex from list of odd vertices

        index_end = random.randint(0, len(odd) - 1)
        end_vertex = odd[index_end]
        del odd[index_end] # Removes vertex from list of odd vertices

        return start_vertex, end_vertex, odd

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
                if vertex != odd[i]:
                    combination.append((vertex, odd[i]))
            if len(combination) > 0:
                possible_pairs.append(combination)

        return possible_pairs

    def shortest_pair_path(self, possible_pairs: List[List[Tuple[str, str]]]) -> Dict:
        """
        Calculates the shortest paths for all possible pairs using Dijkstra's shortest path algorithm.

        Returns them in a dictionary of form paths[(start_vertex, end_vertex)] = {(weight_of_shortest_path, route_taken)}.
        """
        paths: Dict = {}
        
        for list in possible_pairs: # List is the list of [(a, b), (c, d), ...] pairs
            for pair in list:
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
        
        NEEDS OPTIMISATION - What if not ideal combination of pairings (initially) selected?
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

    
    def modify_graph(self, shortest_paths: List[Tuple[str, str, int]]) -> Dict:
        """
        Adds edges from the minimum matching function to the graph. Returns the modified graph.
        
        shortest_paths is a list of form [(start_vertex, end_vertex, weight, route), etc.]
        """
        modified_graph = copy.deepcopy(self.graph)
        for path in shortest_paths: # path is a tuple of form (a, b, c)
            start = path[0]
            end = path[1]
            edge = path[2]
            # If there is already a connection from the start to end vertex, a list of the routes is created
            if end in list(modified_graph[start].keys()): # graph[a]: {b: 3}, {c: 5}, ...
                modified_graph[start][end] = [modified_graph[start][end], modified_graph[start][end]]
                modified_graph[end][start] = [modified_graph[end][start], modified_graph[end][start]]
            else:
                modified_graph[start][end] = edge
                modified_graph[end][start] = edge
        return modified_graph
    
    def check_type(self, obj: Any) -> bool:
        """
        Returns the type if the object is a list or an integer.

        Returns False otherwise.
        """
        if isinstance(obj, list):
            return True
        else:
            return False
        
    def check_bridge(self, graph: Dict, connection: str) -> bool:
        """
        Checks if a connection is a bridge, i.e., it will leave us stranded
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

        if len(non_bridges) < 1: # If the only options are bridges
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
    
    def del_connection(self, current_vertex, possible_connections, min_index):
        """
        Deleted connection in (original) graph so that it can be determined if all
        connections have been visited.
        """
        if self.graph[current_vertex] and possible_connections[min_index] in list(self.graph[current_vertex].keys()):
            del self.graph[current_vertex][possible_connections[min_index]]
            del self.graph[possible_connections[min_index]][current_vertex]

    def walking(self, graph: Dict, total_weight: int, trajectories: List[Tuple[Any, Any]], max_time: int) -> Tuple[Dict, int, List[Tuple[Any, Any]]]:
            """
            Function from step 2 of the algorithm. Returns the circuit of the 
            Euler path and the total weight of the circuit.
            """
            self.stack.append(self.current_vertex)

            # All possible connections from the current vertex
            possible_connections = list(graph[self.current_vertex].keys())
            non_bridges = self.get_non_bridges(graph, possible_connections)

            # Get list of possible edges
            possible_edges = self.get_possible_edges(graph, self.current_vertex, non_bridges)
            #print(self.check_type(possible_edges)
            
            minimum = min(possible_edges) # If there are multiple connections, finds the minimum
            min_index = possible_edges.index(minimum)

            if (total_weight + int(minimum)) > max_time:

                #print(trajectories)
                if trajectories:
                    #print(len(trajectories))
                    length = len(self.stack) - len(trajectories[0][-1])
                    route = self.stack[:-(length+1):-1]
                else:
                    route = self.stack[::-1]
                #print(route)
                """for i in range(1, len(stack) + 1):
                    route.append(stack[-i])"""
                #route.extend(stack[::-1])
                trajectories.append((total_weight, route))
                total_weight = 0
                
            total_weight += int(minimum)  # Adds to the total weight of the circuit
            possible_edges.remove(minimum) # Removes connection as it has been used

            del graph[self.current_vertex][possible_connections[min_index]] # Removes connection from graph
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
        #print("ST", start_vertex)
        modified_graph, total_weight, trajectories = self.walking(modified_graph, total_weight, trajectories, max_time)

        return self.circuit, trajectories
    
    def run_postman(vertices: List[str], graph: Dict, max_time: int) -> Tuple[List[str], List[Tuple[Any, Any]]] :
        """"
        Runs the solution for the postman problem on a given graph.

        Returns the route and the sum of the route.
        """
        postman = Postman(vertices, graph)

        odd = postman.odd_vertices()  # Find odd vertices
        selection = Postman.selection_start(odd)
        start_vertex = selection[0]
        remaining_odd = selection[2]
    
        possible_pairs = Postman.possible_pairs(remaining_odd) # Possible pairs
        shortest_pairs = postman.shortest_pair_path(possible_pairs) # All the shortest paths of the possible pairs
        matching = postman.minimum_matching(shortest_pairs) # Finding minimum matching of shortest paths
        modified_graph = postman.modify_graph(matching) # Add the matching to the original graph

        # Find the euler path for the modified graph
        circuit, trajectories = postman.euler_path(modified_graph, start_vertex, max_time)
        return circuit, trajectories
    
    def calculate_score(trajectories: List[Tuple[str, int]]):
        """
        Returns the score of the route.

        K = the quality of the route, p = fraction of visited connections (between 0 and 1), T = number of trajectories, Min = total travel time
        """
        #p = (len(trajectories) - 1) / total_connections
        p = 1
        
        T = len(trajectories)
        total_weight = 0
        for traj in trajectories:
            total_weight += int(traj[0])
        Min = total_weight
        K = p*10000 - (T*100 + Min)
        return K

    def generate_route(scores: List[str], best_trajectories: Tuple[int, List[Any]], runs: int) -> int:
        """
        Prnts trajectories taken.
        """
        if scores:
            maximum = max(scores)   
            minimum = min(scores)
            average = mean(scores)
            print(f"The maximum score for {runs} runs is {maximum}, the minimum is {minimum}, and the mean is {round(average)}.")
            print("Best route started at %s with %s trajectories." % (best_trajectories[0][1][0], len(best_trajectories)))
            return 1
            """print_route = input("Print trajectories? Choose Y/N. ")
            if print_route.lower() == 'y':
                for trajectory in best_trajectories:
                    print("Trajectory %s, time %s: \n%s" % (best_trajectories.index(trajectory) + 1, trajectory[0], "\n".join(trajectory[1])))
                    print("-------------------------------------------")
                return 1
            else:
                return 1"""
        else:
            print("Path not found in given runs.")
            return 0

    def postman_algorithm(max_time: int, max_trajectories: int, runs: int) -> List[int]:
        """"
        Runs the algorithm for a certain amount of runs, returns the max score
        """
        """vertices = []
        graph = {}
        best_trajectories = ''
        
        for station in Station_Postman:
            graph[station.station_name] = station.connections
            vertices.append(station.station_name)"""
        best_trajectories = ''
        scores = []
        vertices = []
        graph = {}
        for station in Station_Postman:
            graph[station.station_name] = station.connections
            vertices.append(station.station_name)

        for _ in range(runs):
            copy_graph = copy.deepcopy(graph)
            copy_vertices = copy.deepcopy(vertices)
            circuit, trajectories = Postman.run_postman(copy_vertices, copy_graph, max_time)
            #print(len(trajectories), trajectories, '\n\n')
            score = Postman.calculate_score(trajectories)
            if len(trajectories) <= max_trajectories:
                scores.append(score)
                if scores:
                    if score >= max(scores):
                        #print("\nCircuit", circuit, '\n-----')
                        best_trajectories = trajectories
    
        #print(best_trajectories)
        Postman.generate_route(scores, best_trajectories, runs)
        return scores
        