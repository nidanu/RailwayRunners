"""
Algorithm for the Chinese Postman Problem. Makes use of Dijkstra's shortest
path algorithm.
"""
import random
import copy
import sys
from dijkstra import *
from typing import Tuple, Any, Dict
sys.path.append("..")

class Postman():
    """
    Class to tackle the Chinese postman problem.
    """
    def __init__(self, vertices: list[str], graph: Dict) -> None:
        self.vertices: list[str] = vertices 
        self.graph: Dict = graph # {"A": {"B": 1}, "B": {"A": 3, "C": 5} ...}

    def odd_vertices(self) -> list[str]:
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
    
    def selection_start(odd: list[str]) -> Tuple[str, str, list[str]]:
        """
        Randomly selects start and end vertices. The start vertex does not have to 
        equal the end vertex, thus the path is more efficient.
        """
        index_start = random.randint(0, len(odd) - 1)
        start_vertex = odd[index_start]

        # Removes vertex from list of odd vertices
        del odd[index_start]

        index_end = random.randint(0, len(odd) - 1)
        
        end_vertex = odd[index_end]

        # Removes vertex from list of odd vertices
        del odd[index_end]

        return start_vertex, end_vertex, odd


    def possible_pairs(odd: list[str]) -> list[list[Tuple[str, str]]]:
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

    def shortest_pair_path(self, possible_pairs: list[list[Tuple[str, str]]]) -> Dict:
        """
        Calculates the shortest paths for all possible pairs using Dijkstra's shortest path algorithm.

        Returns them in a dictionary of form paths[(start_vertex, end_vertex)] = {(weight_of_shortest_path, route_taken)}.
        """
        paths: Dict[Dict[Tuple(str, int)]] = {}

        # List is the list of [(a, b), (c, d), ...] pairs
        for list in possible_pairs:
            for pair in list:
                
                # Weight of shortest path
                distance, route = Dijkstra.get_results(self.vertices, self.graph, pair[0], pair[1])
                paths[(pair[0], pair[1])] = (distance, route)

        return paths

    def find_min(self, weights: list[int], pairs: Tuple[str, str]) -> Tuple[str, str]:
        """
        Finds the minimum weight of an edge and returns between which vertices this minimum occurs.
        """
        # Find the minimum of all paths for that particular start vertex
        if weights:  
            minimum = min(weights)
            index_min = weights.index(minimum)
            start_v, end_v = pairs[index_min]
        return start_v, end_v
    
    def remove_stations(self, keys: list[str], start_v: str, end_v: str) -> list[str]:
        """
        Removes the stations from the list of possible pairs if they've already been used.
        """
        new_keys = []
        for tpl in keys:
            if tpl[0] != start_v and tpl[0] != end_v and tpl[1] != start_v and tpl[1] != end_v:
                new_keys.append(tpl) 
        return new_keys

    def minimum_matching(self, paths: Dict) -> list[Tuple[str, str, int]]:
        """
        Finds the minimum matching of the shortest paths between uneven vertices. Returns a 
        list of the connections and their weight. 
        
        NEEDS OPTIMISATION - What if not ideal combination of pairings (initially) selected?
        """
        # List of all the start vertices
        keys = list(paths.keys())  
        shortest_paths = []

        while keys:
            start = keys[0][0]

            # List of all pairs with the same start_vertex
            starters = [tpl for tpl in keys if tpl[0] == start] 
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

    
    def modify_graph(self, shortest_paths: list[Tuple[str, str, int]]) -> Dict:
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
            if end in list(modified_graph[start].keys()):
                # graph[a]: {b: 3}, {c: 5}, ...
                original_distance = modified_graph[start][end]
                mutliple_distances = []
                mutliple_distances.append(original_distance)
                mutliple_distances.append(edge)
                modified_graph[start][end] = mutliple_distances
            else:
                modified_graph[start][end] = edge

        return modified_graph
    
    def check_type(self, obj: Any) -> Any:
        """
        Returns the type if the object is a list or an integer.

        Returns False otherwise.
        """
        if isinstance(obj, list):
            return list
        elif isinstance(obj, int):
            return int
        else:
            return False

    def walking(self, graph: Dict, current_vertex: str, stack: list[str], total_weight: int, circuit: list[str]) -> Tuple[Dict, str, list[str], int, list[str]]:
            """
            Function from step 2 of the algorithm. Returns the circuit of the 
            Euler path and the total weight of the circuit.
            """
            stack.append(current_vertex)

            # All possible connections from the current vertex
            possible_connections = list(graph[current_vertex].keys())

            # Minimum edge is selected, and its weight is added to the sum of the circuit
            # List of possible edges to traverse from current_vertex
            possible_edges = [] 
            for key in possible_connections:  
                edge = graph[current_vertex][key]

                # If there are multiple routes for the same pair, finds the minimum
                if self.check_type(edge) == list: 
                    edge = [int(num) for num in edge]
                    connection = int(min(edge))
                else:
                    connection = int(edge)
                possible_edges.append(connection)
                
            # If there are multiple connections, finds the minimum
            if self.check_type(possible_edges) == list: 
                minimum = min(possible_edges)
                min_index = possible_edges.index(minimum)
            elif self.check_type(possible_edges) == int:
                minimum = possible_edges[0]
                min_index = 0

            # Adds to the total weight of the circuit
            total_weight += int(minimum) 
                
            # Removes connection as it has been used
            possible_edges.remove(minimum)

            # Removes vertex from graph
            del graph[current_vertex][possible_connections[min_index]]

            # Neighbouring vertex assigned as the new current vertex
            current_vertex = possible_connections[min_index]

            # If current vertex still has connections to its neighbour(s), process continues to run
            while len(graph[current_vertex]) > 0 and len(stack) > 0:
                graph, current_vertex, stack, total_weight, circuit = self.walking(graph, current_vertex, stack, total_weight, circuit)
                if len(graph[current_vertex]) == 0:
                    circuit.append(current_vertex)
                    current_vertex = stack.pop()
    
            return graph, current_vertex, stack, total_weight, circuit
    
    def euler_path(self, modified_graph: Dict, start_vertex: str) -> Tuple[list[str], int]:
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
        stack = []
        
        # Weight of circuit
        total_weight = 0 
        circuit = []
        current_vertex = start_vertex
        graph, current_vertex, stack, total_weight, circuit = self.walking(modified_graph, current_vertex, stack, total_weight, circuit)

        return circuit, total_weight
    
    def run_postman(vertices: list[str], graph: Dict) -> Tuple[list[str], int] :
        """"
        Runs the solution for the postman problem on a given graph.

        Returns the route and the sum of the route.
        """
        postman = Postman(vertices, graph)

        # Find odd vertices
        odd = postman.odd_vertices()

        selection = Postman.selection_start(odd)
        start_vertex = selection[0]
        remaining_odd = selection[2]
        
        # Possible pairs
        possible_pairs = Postman.possible_pairs(remaining_odd)

        # All the shortest paths of the possible pairs
        shortest_pairs = postman.shortest_pair_path(possible_pairs)

        # Finding minimum matching of shortest paths
        matching = postman.minimum_matching(shortest_pairs)

        # Add the matching to the original graph
        modified_graph = postman.modify_graph(matching)

        # Find the euler path for the modified graph
        route, weight = postman.euler_path(modified_graph, start_vertex)

        return route, weight