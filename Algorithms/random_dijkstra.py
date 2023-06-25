import sys
import random
from typing import List, Tuple
from statistics import mean
sys.path.append("..")
from Classes.station_postman import *
from Algorithms.dijkstra import *

class Quick_dijkstra:

    def __init__(self, vertices, graph):
        self.vertices = vertices
        self.graph = graph

    def selection_start(self) -> Tuple[str, str, List[str]]:
        """
        Randomly selects start and end vertices. The start vertex does not have to 
        equal the end vertex, thus the path is more efficient.
        """
        index_start = random.randint(0, len(self.vertices) - 1)
        start_vertex = self.vertices[index_start]
        index_end = random.randint(0, len(self.vertices) - 1)
        end_vertex = self.vertices[index_end]

        return start_vertex, end_vertex
    
    def all_visited(self, graph: Dict) -> bool:
        """
        Returns True if all connections have been visited.
        """
        keys = list(graph.keys())
        unvisited = 0
        for key in keys:
            if len(graph[key]) > 0:
                unvisited += 1
        if unvisited == 0:
            return True
        else:
            return False
    
    def run_dijkstra(self, max_time):
        total_time = 0
        trajectories = []
        total_trajectories = 0
        while self.all_visited == False:
            start_v, end_v = self.selection_start()
            trajectory_time = 0
            current_trajectory = []
            time, route = Dijkstra.get_results(self.vertices, self.graph, start_v, end_v)
            current_trajectory.append(route)
            if total_time + time > max_time:
                trajectories.append(current_trajectory)
                total_trajectories += 1
                total_time += trajectory_time
                trajectory_time = 0
            trajectory_time += time
        
        return total_time, trajectories, total_trajectories

    def score_time(self, total_time, total_trajectories):
        """
        Returns the score of the route.

        K = the quality of the route, p = fraction of visited connections (between 0 and 1), T = number of trajectories, Min = total travel time
        """
        #p = (len(trajectories) - 1) / total_connections
        p = 1
        
        T = total_trajectories
        Min = total_time
        K = p*10000 - (T*100 + Min)
        return K

    def random_dijkstra(runs, max_time):
        scores = []
        vertices = []
        graph = {}
        
        for station in Station_Postman:
            graph[station.station_name] = station.connections
            vertices.append(station.station_name)
        for _ in range(runs):
            quick_dijk = Quick_dijkstra(vertices, graph)
            total_time, trajectories, total_trajectories = quick_dijk.run_dijkstra(max_time)
            score = quick_dijk.score_time(total_time, total_trajectories)
            scores.append(score)
        
        maximum = max(scores)   
        minimum = min(scores)
        average = mean(scores)

        return maximum, minimum, average