from Classes.station import Station
#from Classes.station_postman import *
from Classes.train import Train
from Classes.station import Station
import matplotlib.pyplot as plt
from scipy import stats
from typing import List, Tuple, NamedTuple


"""
Functions for random algorithm  
"""

def determine_max_routes(num_stations: int) -> int:
    if num_stations == 22:
        return 7
    elif num_stations == 61:
        return 20
    else:
        return None 

def determin_min_routes(num_stations: int) -> int:
    if num_stations == 22:
        return 5
    elif num_stations == 61:
        return 20
    else:
        return None 


def check_progress(runs, total_runs: int, progress: int) -> int:
    if runs % (total_runs // 10) == 0:
        print(f"{progress}%")
        progress += 10
    return progress

def get_next_station(train: Train, stations: List[Station]) -> Station:
    next_station_number = train.choose_next_station()
    next_station_List = [station for station in stations if station.station_number == next_station_number]
    next_station = next_station_List[0]
    return next_station

def check_and_append_visited(next_station: Station, visited: List[str]) -> List[str]:
    if next_station.station_name not in visited:
        visited.append(next_station.station_name)
    return visited

def check_and_append_driven(cur_station: Station, next_station: Station, temp_list_connections: List[List[str]], driven: List[List[str]]) -> List[List[str]]:
    one_way = [cur_station.station_name, next_station.station_name]
    if one_way in temp_list_connections:
        temp_list_connections.remove(one_way)
        driven.append(one_way)
    
    other_way = [next_station.station_name, cur_station.station_name]
    if other_way in temp_list_connections:
        temp_list_connections.remove(other_way)
        driven.append(other_way)
    return driven

def save(train: Train, travel_times: List[int], routes: List[List[str]]) -> Tuple[List[int], List[List[str]]]:
    travel_times.append(train.travel_time)
    routes.append(train.destination_history)
    return travel_times, routes

def reset(train: Train) -> Train:
    train.travel_time_zero()
    train.empty_destination_history()
    return train

def calculate_score(list_connections: List[List[str]], temp_list_connections: List[List[str]], routes: List[List[str]], travel_times: List[int]) -> float:
    n_connections_driven = len(list_connections) - len(temp_list_connections)
    p = n_connections_driven / len(list_connections)
    T = len(routes)
    Min = sum(travel_times)
    K = p * 10000 - (T * 100 + Min)
    return K

class ScoresAndRoutes(NamedTuple):
    scores: List[float]
    routes: List[List[str]]
    some_list: List[int]
    another_list: List[List[str]]
    additional_list: List[str]
    yet_another_list: List[List[str]]

def process_scores_and_routes(scores_and_routes: ScoresAndRoutes) -> Tuple[List[float], List[List[str]], int, List[int]]:
    scores_and_routes.sort(key=lambda x: x[0])
    
    scores = []
    for score_and_route in scores_and_routes:
        scores.append(score_and_route[0])
    
    top_route = scores_and_routes[-1][1]
    top_travel_time = scores_and_routes[-1][2]
    
    top_travel_times = []
    
    return scores, top_route, top_travel_time, top_travel_times 

def print_fastest_journey(top_route: List[List[str]], top_travel_time: List[int]) -> List[List[int]]:
    print(" =" * 40)
    print("Fastest journey:")
    print(f"Starting station: {top_route[0][0]}")
    
    for i in range(len(top_route)):
        print(f"Route: {i + 1}" + " -" * 20)
        for destinations in top_route[i]:
            print(f"{destinations}")  # Visited station:
        print(f"Total time route: {top_travel_time[i]}\n")
        
    top_travel_times = top_travel_time[:]  
    
    return top_travel_times 
    
def print_connections(scores_and_routes: ScoresAndRoutes) -> None:
    # Prints the driven connections
    print("Driven:")
    for connection in scores_and_routes[-1][3]:
        print(f"{connection[0]} <-> {connection[1]}")
    print()
    
    # Prints not driven connections
    print("Not driven:")
    for connection in scores_and_routes[-1][5]:
        print(f"{connection[0]} <-> {connection[1]}")
    print()

def print_scores(scores: List[int]) -> None:
    # Prints high scores
    print("High scores:")
    for high_score in scores[-5:]:
        print(high_score)
    print()

    # Prints low scores 
    print("Low scores:")
    for low_score in scores[:5]:
        print(low_score)
    print()

def print_stats(min_time: int, top_travel_times: List[int], max_routes: int, top_route: List[List[str]], num_connections: int, scores_and_routes: ScoresAndRoutes, num_stations: int) -> None:
    print(f"Min time: {min_time}")
    print(f"Top time: {sum(top_travel_times)}")
    print(f"Max routes: {max_routes}")
    print(f"Top Routes: {len(top_route)}")
    print(f"Max driven: {num_connections}")
    print(f"Top driven: {len(scores_and_routes[-1][3])}")
    print(f"Max visited: {num_stations}")
    print(f"Top visited: {len(scores_and_routes[-1][4])}")
    print()

def print_scores_stats(num_stations: int, min_time: int, scores: List[float]) -> None:
    if num_stations == 22:
        print(f"Max score: {10000 - ((min_time // (2*60) + 1)*100 + min_time)}")
    elif num_stations == 61:
        print(f"Max score: {10000 - ((min_time // (3*60) + 1)*100 + min_time)}")
    
    top_score = max(scores)
    print(f"Top score: {top_score}")
    
    avg_score = sum(scores) / len(scores)
    print(f"Avg score: {avg_score}")
    print()

def print_program_stats(total_runs: int, duration: float) -> None:
    print(f"Runs: {total_runs}")
    print("Program duration:", duration, "seconds")
    print()
    
def run_tests_and_draw_histogram(scores: List[float]) -> None:
    from scipy import stats
    import numpy as np

    # Shapiro-Wilk Test
    shapiro_test = stats.shapiro(scores)
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}")
    print(f"P-value: {shapiro_test.pvalue}")
    
    def draw_histogram(data, bins):
        plt.hist(data, bins=bins, edgecolor='black')
        plt.xlabel("Scores")
        plt.ylabel("Frequency")
        plt.title("Random Algorithm 100,000 runs")
        plt.savefig("hist_test.png")
        plt.close()

    # Example usage
    my_data = scores
    num_bins = 16
    draw_histogram(my_data, num_bins)

