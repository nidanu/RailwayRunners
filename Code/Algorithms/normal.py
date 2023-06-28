"""
Name: normal

By: Railway Runners

Does: random algoythm  for x amount of runs
"""
import random
import time
from Code.functions import *

# Runs random algorithm for x amount of times  
def normal(num_stations, num_connections, stations, list_connections, min_time):
    # Set variables for big loop
    max_routes, max_expected, best_start_station = determine_max_routes(num_stations) 
    min_routes, min_expected, time_per_route = determin_min_routes(num_stations)
    previous_score, progress, runs, scores_and_routes = 0, 0, 0, []
    algorithm_name = "normal"
    
    # Ask user for input 
    total_runs = int(input("How many runs? "))
    with_tests = input("Want statistics?[yes/no]")
    printout = input("Printout text file?[yes/no]")
    
    start_time = time.time()
    
    # Determines when to stop
    while runs <= total_runs:
        
        # Print progress in %
        if runs >= 10:
            progress = check_progress(runs, total_runs, progress)
        
        # Create Train object with random start station
        train = Train((stations[random.randint(0, len(stations) - 1)]))        
        
        # Set initial variables for single run
        visited = [train.current_station.station_name]
        temp_list_connections = list(list_connections)
        cur_station = train.current_station
        driven, n_routes, routes, travel_times = [], 1, [], []
        
        # Move train till all connections visited or out of routes
        while n_routes <= max_routes and len(temp_list_connections) != 0: 
            
            # Changes station until route time limit reached
            cur_station, visited, driven = run_routes(temp_list_connections, train, stations, visited, driven, cur_station, time_per_route)
                        
            # Save and reset single run 
            travel_times, routes = save(train, travel_times, routes) 
            train = reset(train)
            n_routes += 1

            # Sets first station of route to random station
            next_station = get_next_station(train, stations)
            
            # Calculate score and write to file
            score = calculate_score(list_connections, temp_list_connections, routes, travel_times)
            previous_score = write_to_files(score, previous_score, routes, visited, driven, printout, algorithm_name)
        
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