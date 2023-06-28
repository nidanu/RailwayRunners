"""
Name: max

By: Railway Runners

Does: random algoythm + only maximum scores  of routes for x amount of times
"""
import time
from Code.functions import *

def max(num_stations, num_connections, stations, list_connections, min_time):
    # Set variables for big loop
    min_routes = determin_min_routes(num_stations)
    max_routes = determine_max_routes(num_stations) 
    total_runs = int(input("How many runs? "))
    scores_and_routes = [] 
    progress = 0
    runs = 0
    previous_score = 0
    i = 0
    
    start_time = time.time()
    score = 0
    while runs <= total_runs:
        n_routes = 1
        temp_list_connections = ["start"]
        cur_highscore = 1.0
        
        # Loop that only searches for minimal route length journeys
        while n_routes <= min_routes or len(temp_list_connections) != 0: #or score > 8300:
            
            # Create Train object with random start station
            #if runs in list(range(0, num_stations*10000, 10000)):       
            #    print(f"station {i}:")
            train = Train(stations[11])#Train((stations[random.randint(0, len(stations) - 1)]))
            #    previous_score = 0
            #    i += 1
                
            # Move train till all stations are visited or out of routes or route travel_time >= 120
            visited = [train.current_station.station_name]
            temp_list_connections = list(list_connections)
            cur_station = train.current_station
            travel_times = []
            n_routes = 1
            routes = []
            driven = []

            while n_routes <= min_routes and len(temp_list_connections) != 0: 
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
                score = calculate_score(list_connections, temp_list_connections, routes, travel_times)
                if score > previous_score: #and score > 8000:
                    previous_score = score
                    print(score)
                
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
    #run_tests_and_draw_histogram(scores)   
