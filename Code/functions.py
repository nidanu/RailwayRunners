from Classes.station import Station
#from Classes.station_postman import *
from Classes.train import Train
from Classes.station import Station
import matplotlib.pyplot as plt
#from scipy import stats
from typing import List, Tuple, NamedTuple

import time
import random

"""
Functions for random algorithm  
"""

# select case statistics
def determine_max_routes(num_stations: int) -> int:
    if num_stations == 22:
        return 7, 9000, 11
    elif num_stations == 61:
        return 20, 4000, 42
    else:
        return None 

# selects minimum case statistics
def determin_min_routes(num_stations: int) -> int:
    if num_stations == 22:
        return 5, 8000, 120
    elif num_stations == 61:
        return 20, 3200, 180
    else:
        return None 

# Checks progress in %
def check_progress(runs: int, total_runs: int, progress: int) -> int:
    if runs % (total_runs // 10) == 0:
        print(f"{progress}%")
        progress += 10
    return progress

# Randomly selects next station
def get_next_station(train: Train, stations: List[Station]) -> Station:
    next_station_number = int(train.choose_next_station())
    next_station_List = [station for station in stations if station.station_number == next_station_number]
    next_station = next_station_List[0]
    return next_station

# Checks and adjusts visited based on next station
def check_and_append_visited(next_station: Station, visited: List[str]) -> List[str]:
    if next_station.station_name not in visited:
        visited.append(next_station.station_name)
    return visited

# Checks and adjusts driven  based on current and next station
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

# Saves 1 journey train data
def save(train: Train, travel_times: List[int], routes: List[List[str]]) -> Tuple[List[int], List[List[str]]]:
    travel_times.append(train.travel_time)
    routes.append(train.destination_history)
    return travel_times, routes

# Resets train after 1 journey
def reset(train: Train) -> Train:
    train.travel_time_zero()
    train.empty_destination_history()
    return train

# Calculates score
def calculate_score(list_connections: List[List[str]], temp_list_connections: List[List[str]], routes: List[List[str]], travel_times: List[int]) -> float:
    
    n_connections_driven = len(list_connections) - len(temp_list_connections)
    p = n_connections_driven / len(list_connections)
    T = len(routes)
    Min = sum(travel_times)
    
    K = p * 10000 - (T * 100 + Min)
    return K

# Creates seperate datatype for scores_and_routes list
class ScoresAndRoutes(NamedTuple):
    scores: List[float]
    routes: List[List[str]]
    some_list: List[int]
    another_list: List[List[str]]
    additional_list: List[str]
    yet_another_list: List[List[str]]

# Filters and sorts data from runs 
def process_scores_and_routes(scores_and_routes: ScoresAndRoutes) -> Tuple[List[float], List[List[str]], int, List[int]]:
    
    # sorts scores_and_routes based on score
    scores_and_routes.sort(key=lambda x: x[0])
    
    # creates list of scores
    scores = []
    for score_and_route in scores_and_routes:
        scores.append(score_and_route[0])
    
    # Determines top route, travel time and creates list for
    top_route = scores_and_routes[-1][1]
    top_travel_time = scores_and_routes[-1][2]
    top_travel_times = []
    
    return scores, top_route, top_travel_time, top_travel_times 

# Prints name of the sequence of stations travled for the best route
def print_fastest_journey(top_route: List[List[str]], top_travel_time: List[int]) -> List[List[int]]:
    
    # prints header
    print(" =" * 40)
    print("Fastest journey:")
    print(f"Starting station: {top_route[0][0]}")
    
    # Prints routes seperately
    for i in range(len(top_route)):
        print(f"Route: {i + 1}" + " -" * 20)
        for destinations in top_route[i]:
            print(f"{destinations}")  # Visited station:
        print(f"Total time route: {top_travel_time[i]}\n")
        
    top_travel_times = top_travel_time[:]  
    
    return top_travel_times 

# prints the connections driven and the connections not driven
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

# Prints high and low scores
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

# Prints total run statistics
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

# Prints different highest theoreticsl score based on case
def print_scores_stats(num_stations: int, min_time: int, scores: List[float]) -> None:
    # determine case and calculate highest score
    if num_stations == 22:
        print(f"Max score: {10000 - ((min_time // (2*60) + 1)*100 + min_time)}")
    elif num_stations == 61:
        print(f"Max score: {10000 - ((min_time // (3*60) + 1)*100 + min_time)}")
    
    # prints top score and avarige score
    top_score = max(scores)
    print(f"Top score: {top_score}")
    avg_score = sum(scores) / len(scores)
    print(f"Avg score: {avg_score}")
    print()

# Prints information about the program duration 
def print_program_stats(total_runs: int, duration: float) -> None:
    print(f"Runs: {total_runs}")
    print("Program duration:", duration, "seconds")
    print()

# Does statistics and draws histogram
def run_tests_and_draw_histogram(scores: List[float]) -> None:
    # imports libraries 
    from scipy import stats
    import numpy as np

    # Does Shapiro-Wilk Test
    shapiro_test = stats.shapiro(scores)
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}")
    print(f"P-value: {shapiro_test.pvalue}")
    
    # creates histogram function
    def draw_histogram(data, bins):
        plt.hist(data, bins=bins, edgecolor='black')
        plt.xlabel("Scores")
        plt.ylabel("Frequency")
        plt.title("Random Algorithm 100,000 runs")
        plt.savefig("hist_test.png")
        plt.close()

    # Inputs data for histogram drawing
    my_data = scores
    num_bins = 16
    draw_histogram(my_data, num_bins)

# Writes results to text files
def write_to_files(score: float, previous_score: float, routes: List[List[str]],visited: List[str], driven: List[List[str]], printout: str, algorithm_name: str) -> float:
    if printout.lower() == "yes":
        random_number = random.randint(1, 20000)
        if random_number == 1:
            with open("Results/" + algorithm_name + "_random_scores.txt", "a") as f:
                f.write(str(score) + "\n")
            
        # writes highest scores to text file
        if score > previous_score: #and score > min_expected:
            previous_score = score
            print(score)
            with open("Results/" + algorithm_name + "_higher_scores_n.txt", "a") as f:
                f.write(str(score) + "\n")
                f.write(str(routes) + "\n")
                f.write(str(visited) + "\n")
                f.write(str(driven) + "\n")
        return previous_score

# Runs random algorithm with max variables 
def run_random_max(score: float, min_routes: int, temp_list_connections: List[List[str]], train: Train, stations: List[Station], visited: List[str], driven: List[List[str]], cur_station: Station, list_connections: List[List[str]], travel_times: List[int], n_routes: int, routes: List[List[str]], previous_score: float, min_expected: int, max_expected: int, time_per_route: int, runs: int, num_stations: int, printout: str) -> Tuple[int, int, List[List[str]]]:
    # Runs entire random loop with minimal amount of routes
    while n_routes <= min_routes and len(temp_list_connections) != 0:
        
        # Makes train drive randomly until route time is satisfied
        while train.travel_time <= time_per_route:
            # Pick random next station from station connections
            next_station = get_next_station(train, stations)

            # End route if travel_time > 120, else move to next station                
            if (train.travel_time + train.current_station.connections[str(next_station.station_number)]) > time_per_route:
                break
            else:
                # Update current train object
                train.update_travel_time(next_station)            
                train.add_destination_to_history(next_station)                    
                
                # Updates visited and driven
                visited = check_and_append_visited(next_station, visited)
                driven = check_and_append_driven(cur_station, next_station, temp_list_connections, driven)
            
            cur_station = next_station
                
        # Save and reset
        travel_times, routes = save(train, travel_times, routes) 
        train = reset(train)

        # Sets first station of route to random station
        next_station = get_next_station(train, stations)
        
        n_routes += 1
        
        # Calculates and saves scores
        score = calculate_score(list_connections, temp_list_connections, routes, travel_times)
        previous_score = write_to_files(score, previous_score, routes, visited, driven, printout)
                    
    return previous_score, n_routes, temp_list_connections

# Makes train drive randomly until route time is satisfied
def run_routes(temp_list_connections: List[List[str]], train: Train, stations: List[Station], visited: List[str], driven: List[List[str]], cur_station: Station, time_per_route: int) -> Tuple[Station, List[str], List[List[str]]]:
    while train.travel_time <= time_per_route:

        # Pick random next station from station connections
        next_station = get_next_station(train, stations)

        # End route if travel_time > 120, else move to next station                
        if (train.travel_time + train.current_station.connections[str(next_station.station_number)]) > time_per_route:
            break
        else:
            # Update current train object
            train.update_travel_time(next_station)            
            train.add_destination_to_history(next_station)                    
            
            # Updates visited and driven
            visited = check_and_append_visited(next_station, visited)
            driven = check_and_append_driven(cur_station, next_station, temp_list_connections, driven)
        
        cur_station = next_station
        
    return cur_station, visited, driven

