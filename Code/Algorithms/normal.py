import random
import time
from functions import *

def normal(num_stations, num_connections, stations, list_connections, min_time):
    # Set variables for big loop
    max_routes = determine_max_routes(num_stations) 
    total_runs = int(input("How many runs? "))
    scores_and_routes = [] 
    progress = 0
    runs = 0
    
    start_time = time.time()

    while runs <= total_runs:
        
        # Progress printer 
        progress = check_progress(runs, total_runs, progress)
        
        # Create Train object with random start station
        train = Train((stations[random.randint(0, len(stations) - 1)]))        
        
        # Move train till all stations are visited or out of routes or route travel_time >= 120
        visited = [train.current_station.station_name]
        temp_list_connections = list(list_connections)
        cur_station = train.current_station
        travel_times = []
        n_routes = 1
        routes = []
        driven = []

        while n_routes <= max_routes and len(temp_list_connections) != 0: # -------------------------------------
        # while (n_routes <= max_routes) and (len(visited) <= len(stations)):
            while train.travel_time <= 120:

                # Pick random next station from station connections
                next_station = get_next_station(train, stations)

                # End route if travel_time > 120, else move to next station                
                if (train.travel_time + train.current_station.connections[next_station.station_number]) > 120:
                    break
                else:
                    # Update current train object
                    train.update_travel_time(next_station)            
                    train.add_destination_to_history(next_station)                    
                    
                    # Updates visited and driven
                    visited = check_and_append_visited(next_station, visited)
                    driven = check_and_append_driven(cur_station, next_station, temp_list_connections, driven)
                
                cur_station = next_station
            
            # Sets first station of route to random station
            next_station = get_next_station(train, stations)
            
            # Save and reset
            travel_times, routes = save(train, travel_times, routes) 
            train = reset(train)
            
            n_routes += 1
        
        # Calculate and store traval data
        score = calculate_score(list_connections, temp_list_connections, routes, travel_times)
        scores_and_routes.append([score, routes, travel_times, driven, visited, temp_list_connections]) 
            
        runs += 1
    
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
    
    # Does statistics
    run_tests_and_draw_histogram(scores)   