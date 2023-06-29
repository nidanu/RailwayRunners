#!/usr/bin/env python 
"""
Runs the Postman Tour algorithm & calculates the score.
"""
import random
import copy
from statistics import mean
from typing import List, Dict, Tuple, Any
from Code.Classes.postman import Postman
from Code.Classes.station_postman import Station_Postman

def run_postman(vertices: List[str], graph: Dict, max_time: int) -> Tuple[List[str], List[Tuple[Any, Any]]] :
    """"
    Runs the solution for the postman problem on a given graph.

    Returns the route and the sum of the route.
    """
    postman = Postman(vertices, graph)

    # Find odd vertices
    odd = postman.odd_vertices() 
    index_start = random.randint(0, len(odd) - 1)
    start_vertex = odd[index_start]

    # Possible pairs
    possible_pairs = Postman.possible_pairs(odd) 

    # All the shortest paths of the possible pairs
    shortest_pairs = postman.shortest_pair_path(possible_pairs) 

    # Finding minimum matching of shortest pathss
    matching = postman.minimum_matching(shortest_pairs) 

    # Add the matching to the original graph
    modified_graph = postman.modify_graph(matching)

    # Find the euler path for the modified graph
    circuit, trajectories = postman.euler_path(modified_graph, start_vertex, max_time)
    return circuit, trajectories
    
def calculate_score(trajectories: List[Tuple[str, int]]):
    """
    Returns the score of the route.

    K = the quality of the route, p = fraction of visited connections (between 0 and 1), T = number of trajectories, Min = total travel time
    """
    p = 1
    
    T = len(trajectories)
    total_weight = 0
    for traj in trajectories:
        total_weight += int(traj[0])
    Min = total_weight

    K = p*10000 - (T*100 + Min)
    return K

def generate_route(scores: List[str]) -> Tuple[int, int, int]:
    """
    Finds the maximum, minimum, and average score.
    """
    if scores:
        maximum = max(scores)   
        minimum = min(scores)
        average = mean(scores)

        return maximum, minimum, average

    else:
        print("Path not found in given runs.")
        return 0

def postman_algorithm(max_time: int, max_trajectories: int) -> List[int]:
    """"
    Runs the algorithm until a keyboard interrupt.
    """
    best_trajectories = ''
    scores = []
    vertices = []
    graph = {}
    for station in Station_Postman:
        graph[station.station_name] = station.connections
        vertices.append(station.station_name)
    print("Running postman tour.")

    while True:
        try: 
            copy_graph = copy.deepcopy(graph)
            copy_vertices = copy.deepcopy(vertices)
            circuit, trajectories = run_postman(copy_vertices, copy_graph, max_time)
            score = calculate_score(trajectories)

            if len(trajectories) <= max_trajectories:
                scores.append(score)
                if scores:
                    if score >= max(scores):
                        best_trajectories = trajectories

        except KeyboardInterrupt:            
            maximum, minimum, average = generate_route(scores)
            with open('Results/postman.txt', 'w') as f:
                f.write("Maximum: %s\n" % maximum)
                f.write("Minimum: %s\n" % minimum)
                f.write("Average: %s\n" % round(average))
                f.write(str(scores))
                return best_trajectories
    