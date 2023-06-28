"""
Name: max

By: Railway Runners

Does: random algorithm + only maximum scores selection  for x amount of runs.
"""
import random
import time
from Code.functions import *

def max(num_stations, num_connections, stations, list_connections, min_time):
    # Set variables for big loop
    max_routes, max_expected, best_start_station = determine_max_routes(num_stations)
    min_routes, min_expected, time_per_route = determin_min_routes(num_stations)
    i, previous_score, progress, runs, score, scores_and_routes = 0, 0, 0, 0, 0, [] 
    algorithm_name = "max"
    
    # Ask user for input
    total_runs = int(input("How many runs? "))
    with_tests = input("Want statistics?[yes/no]")
    printout = input("Printout text file?[yes/no]")
    
    start_time = time.time()
     
    while runs <= total_runs:
        # Set starting variables 
        cur_highscore, n_routes, temp_list_connections = 1.0, 1, ["start"]
        
        # Loop that only searches for minimal route length journeys
        while n_routes <= min_routes or len(temp_list_connections) != 0: #or score > 8300:
            
            # Starts the train with optimal starting station per case 
            train = Train(stations[best_start_station])
                
            # Move train till all stations are visited or out of routes or route travel_time >= 120
            visited = [train.current_station.station_name]
            temp_list_connections = list(list_connections)
            cur_station = train.current_station
            driven, travel_times, routes, n_routes = [], [], [], 1
            
            # Runs entire random loop
            previous_score, n_routes, temp_list_connections  = run_random_max(score, min_routes, temp_list_connections, train, stations, visited, driven, cur_station, list_connections, travel_times, n_routes, routes, previous_score, min_expected, max_expected, time_per_route, runs, num_stations, printout, algorithm_name, algorithm_name)
            
            # Calculate and store traval data
            score = calculate_score(list_connections, temp_list_connections, routes, travel_times)
            scores_and_routes.append([score, routes, travel_times, driven, visited, temp_list_connections]) 
            
            runs += 1
    
    # Record dureation
    end_time = time.time() 
    duration = end_time - start_time

    # Filters data from scores_and_routes
    scores, top_route, top_travel_time, top_travel_times = process_scores_and_routes(scores_and_routes)
    
    # Prints results 
    top_travel_times = print_fastest_journey(top_route, top_travel_time)
    print_connections(scores_and_routes)
    print_scores(scores)
    print_stats(min_time, top_travel_times, max_routes, top_route, num_connections, scores_and_routes, num_stations)
    print_scores_stats(num_stations, min_time, scores)
    print_program_stats(total_runs, duration)
    
    # Does tests and draws graphs
    if with_tests.lower() == "yes":
        run_tests_and_draw_histogram(scores)   
    