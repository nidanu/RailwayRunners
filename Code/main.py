#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""

import random
import time
import sys 
sys.path.append('..')

from Algorithms.bridges import Graph  
from Algorithms.greedy import greedy 
from Classes.station import Station
from Classes.train import Train
from Code.functions import *
from typing import List


# Create list with all stations + connections
stations = create_list_of_stations("../Cases/Holland/StationsHolland.csv")
create_station_connections("../Cases/Holland/StationsHolland.csv", "../Cases/Holland/ConnectiesHolland.csv", stations) 

# Count number of stations
with open("../Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())
    
# Count number of connections
with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)   
    num_connections = len(f.readlines())   
    
# Creates list of connections 
with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)
    list_connections = []
    list_connection_lengths = []
    for connection in f.readlines():
        cur_connection = connection.split(",")
        clean_connection = cur_connection[0:2]
        list_connections.append(clean_connection)    
        list_connection_lengths.append(int(cur_connection[2]))
    min_time = sum(list_connection_lengths)

# Ask for test input
print("Styles:\n- normal\n- single\n- max\n- heur\n- greedy\n- 7")
style = input("What style of test? ")

# Contains all styles of tests 
if style.lower() == "max":
    # find in main save
    pass
    

elif style.lower() == "single":
    # Create Train object with random start station
    train = Train((stations[random.randint(0, len(stations) - 1)]))    

    # Set starting variables 
    max_routes = determine_max_routes(num_stations)
    temp_list_connections = list(list_connections)
    visited = [train.current_station.station_name]
    cur_station = train.current_station
    travel_times = []
    n_routes = 1
    routes = []
    driven = [] 
            
    start_time = time.time() 
    
    # Move train till all stations are visited or out of routes or route travel_time >= 120
    while n_routes <= max_routes and len(list_connections) != 0: # -------------------------------------
        while train.travel_time <= 120:

            # Pick random next station from station connections
            next_station_number = train.choose_next_station()
            next_station_List = [station for station in stations if station.station_number == next_station_number]
            next_station = next_station_List[0]            
            
            # End route if travel_time > 120, else move to next station
            if (train.travel_time + train.current_station.connections[next_station.station_number]) > 120:
                break
            else:
                # Update total travel time of train
                train.update_travel_time(next_station)                

                # Add next station to travel history and move towards it
                train.add_destination_to_history(next_station)
                
                # Saves visited stations
                if next_station.station_name not in visited:
                    visited.append(next_station.station_name)
                
                # --------------------------------------------------------------------------
                one_way = [cur_station.station_name, next_station.station_name]
                if one_way in temp_list_connections:
                    temp_list_connections.remove(one_way)
                    driven.append(one_way)
                other_way = [next_station.station_name, cur_station.station_name]
                if other_way in temp_list_connections:
                    temp_list_connections.remove(other_way)
                    driven.append(other_way)
            cur_station = next_station
        new_start_station_number = train.choose_next_station()
        new_start_station_List = [station for station in stations if station.station_number == new_start_station_number]
        train.current_station = new_start_station_List[0]            

        train.current_station
        # Save route specific information
        travel_times.append(train.travel_time)
        routes.append(train.destination_history)
        train.travel_time_zero()
        train.empty_destination_history()
        n_routes += 1        
    
    # ----------------------------------------------------------------------------
    end_time = time.time() 
    duration = end_time - start_time
    
    # Print routes
    print(" =" * 40)    
    for i in range(len(routes)):        
        print()
        print(f"Route: {i + 1}" + " -" * 20)
        for destinations in routes[i]:
            print(f"{destinations}")  # Visited station:            
        print(f"Total time route: {travel_times[i]}")        

    # Create list with all station names 
    not_visited = []
    for station in stations:
        not_visited.append(station.station_name)
    print()

    # Print list of all visited stations
    print("Visited:")
    for been_there in visited:
        print(been_there)
        if been_there in not_visited:
            not_visited.remove(been_there)
    print()

    #------------------------------------------------------------
    print("Driven:")
    for connection in driven:
        print(f"{connection[0]} <-> {connection[1]}")
    print()

    # Print list of all NOT visited stations
    print("Not visited:")
    for station_name in not_visited:
        print(station_name)
    print()

    #----------------------------------------------------------------------------------
    print("Not driven:")
    for connection in temp_list_connections:
        print(f"{connection[0]} <-> {connection[1]}")
    print()
    
    # Print travel statistics
    print(f"Visited: {len(visited)}")
    print(f"Driven: {len(driven)}") #---------------------------------------------------
    print(f"NOT visited: {len(not_visited)}")
    print(f"NOT driven: {len(temp_list_connections)}") #-----------------------------------------------------
    print()
    
    # Calculate score
    #---------------------------------------------------------------------------
    n_connections_driven = len(list_connections) - len(temp_list_connections)
    p = n_connections_driven/len(list_connections)
    
    T = n_routes - 1
    Min = sum(travel_times)
    K = p*10000 - (T*100 + Min)
    
    # Print statistic
    print(f"Routes: {T}")
    print(f"Total time: {sum(travel_times)}")
    print("Program duration:", duration, "seconds")
    print(f"Score: {K}")

# Runs random for x amount of times    
elif style.lower() == "normal":
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

elif style == "heur":
    # Set variables for big loop
    scores_and_routes = [] 
    progress = 0
    total_runs = int(input("How many runs? "))
    runs = 0
    
    if num_stations == 22:
        max_routes = 7
    elif num_stations == 61:
        max_routes = 20
    
    start_time = time.time() # ----------------------------------------------
    
    while runs <= total_runs:
        
        # Progress printer 
        if (runs % (total_runs/10) == 0):
            print(f"{progress}%")
            progress += 10        

        # Create Train object with random start station
        train = Train((stations[random.randint(0, len(stations) - 1)]))        
        
        # Move train till all stations are visited or out of routes or route travel_time >= 120
        n_routes = 1
        travel_times = []
        routes = []
        visited = [train.current_station.station_name]
        # ---------------------------------------------------------------------------------------------------------------------
        driven = []
        temp_list_connections = list(list_connections)
        cur_station = train.current_station
        
        while n_routes <= max_routes and len(temp_list_connections) != 0: # -------------------------------------
        # while (n_routes <= max_routes) and (len(visited) <= len(stations)):
            while train.travel_time <= 120:

                # Pick random next station from station connections
                next_station_number = train.choose_next_station()
                next_station_List = [station for station in stations if station.station_number == next_station_number]
                next_station = next_station_List[0]

                # End route if travel_time > 120, else move to next station                
                if (train.travel_time + train.current_station.connections[next_station.station_number]) > 120:
                    break
                else:
                    # Update total travel time of train
                    train.update_travel_time(next_station)            
                    
                    # Add next station to travel history and move towards it
                    train.add_destination_to_history(next_station)                    
                    
                    if next_station.station_name not in visited:
                        visited.append(next_station.station_name)
                    
                    # Maintains a list of untravled connections
                    one_way = [cur_station.station_name, next_station.station_name]
                    if one_way in temp_list_connections:
                        temp_list_connections.remove(one_way)
                        driven.append(one_way)
                    other_way = [next_station.station_name, cur_station.station_name]
                    if other_way in temp_list_connections:
                        temp_list_connections.remove(other_way)
                        driven.append(other_way)
                cur_station = next_station
            
            # Sets first station of route to random station
            new_start_station_number = train.choose_next_station()
            new_start_station_List = [station for station in stations if station.station_number == new_start_station_number]
            train.current_station = new_start_station_List[0]            
                    
            
            # Save and reset
            travel_times.append(train.travel_time)
            routes.append(train.destination_history)
            train.travel_time_zero()
            train.empty_destination_history()
            n_routes += 1
        
        # Calculate and store scores
        # ------------------------------------------------------------------------
        n_connections_driven = len(list_connections) - len(temp_list_connections)
        p = n_connections_driven/len(list_connections)

        T = len(routes)
        Min = sum(travel_times)
        K = p*10000 - (T*100 + Min)
        scores_and_routes.append([K, routes, travel_times, driven, visited, temp_list_connections]) 
            
        runs += 1
    
    # ----------------------------------------------------------------------------------------------------
    end_time = time.time() 
    duration = end_time - start_time
    
    # Sorts and separates output
    scores_and_routes.sort(key=lambda x: x[0])
    scores = [] 
    for score_and_route in scores_and_routes:
        scores.append(score_and_route[0])

    # Print max route with travel time
    top_route = scores_and_routes[-1][1]
    top_travel_time = scores_and_routes[-1][2]
    top_travel_times = []
    
    print(" =" * 40)
    print("Fastest journey:")
    print(f"Starting station: {top_route[0][0]}")
    print()

    for i in range(len(top_route)):
        print(f"Route: {i + 1}" + " -" * 20)
        for destinations in top_route[i]:
            print(f"{destinations}")  # Visited station:
        print(f"Total time route: {top_travel_time[i]}\n")
        top_travel_times.append(top_travel_time[i])

    # Prints top scores
    top_scores = scores[-5:]
    print("Top scores:")
    for top_score in top_scores:
        print(top_score)
    print()

    # Prints low scores 
    low_scores = scores[:5]
    print("Low scores:")
    for low_score in low_scores:
        print(low_score)
    print()
    
    # Prints not visited connections
    print("Not driven:")
    for connection in scores_and_routes[-1][5]:
        print(f"{connection[0]} <-> {connection[1]}")
    print()    

    # Prints avarage and max scores
    print(f"Min time: {min_time}")
    print(f"Top time: {sum(top_travel_times)}")
    print(f"Max routes: {max_routes}")
    print(f"Top Routes: {len(top_route)}")
    print(f"Max driven: {num_connections}")
    print(f"Top driven: {len(scores_and_routes[-1][3])}")
    print(f"Max visited: {num_stations}")
    print(f"Top visited: {len(scores_and_routes[-1][4])}")
    print()
    
    # Print top and avg score
    if num_stations == 22:
        print(f"Max score: {10000 - ((min_time // (2*60) + 1)*100 + min_time)}")
    if num_stations == 61:
        print(f"Max score: {10000 - ((min_time // (3*60) + 1)*100 + min_time)}")
    top_score = max(scores)
    print(f"Top score: {top_score}")
    avg_score = sum(scores)/len(scores)
    print(f"Avg score: {avg_score}")
    print()
    
    # Program statistics 
    print(f"Runs: {total_runs}")
    print("Program duration:", duration, "seconds")
    print()
    
    with open("test_random_less_routes.txt", "a") as f:
        f.write(f"Routes: {max_routes}\n Highscore: {max(scores)}\n Average: {avg_score}\n")
    
    
    """
    Tests
    """
    # ===================================================
    from scipy import stats
    import numpy as np

    # Shapiro-Wilk Test
    shapiro_test = stats.shapiro(scores)
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}")
    print(f"P-value: {shapiro_test.pvalue}")
    
    import matplotlib.pyplot as plt

    def draw_histogram(data, bins):
        plt.hist(data, bins=bins, edgecolor='black')
        plt.xlabel("Scores")
        plt.ylabel("Frequency")
        plt.title("Random Algoritme 100.000 runs")
        plt.savefig("hist_test.png")
        plt.close()

    # Example usage
    my_data = scores
    num_bins = 16
    draw_histogram(my_data, num_bins)
    

elif style == "7":
    # Create variables for score calculations
    top_score = 0 
    average_score = 0 
    average_time = 0  

    # Create network starting from each available station and calculate network score
    for l in range(num_stations):  
        # Create empty Graph and print starting station route              
        g = Graph(num_stations, l) 
        print(f" -" * 20)             
        print(f"Starting station: {stations[g.starting_station].station_name} \n")

        # Load all connections into Graph
        with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
            next(f)       
            for i in range(num_connections):
                connection_str = f.readline()
                connection = connection_str.split(",")
        
                station_1 = connection[0]
                station_2 = connection[1]            
            
                for j in range(num_stations):
                    if stations[j].station_name == station_1:
                        save_station_1 = j                    
                    if stations[j].station_name == station_2:
                        save_station_2 = j
                    
                g.addEdge(save_station_1, save_station_2)
                g.addEdge(save_station_2, save_station_1)

        # Print calculated Graph, score and network total time    
        
        g.printEulerTour()	
        print()
        print(f"Score: {g.final_score}")
        print(f"Total time: {g.total_time_network}")   

        # Add score and time to variables to calculate overall average
        average_score += g.final_score
        average_time += g.total_time_network
        
        # Compare all scores for highest result, and save station number of best station
        if g.final_score > top_score:
            top_score = g.final_score
            top_station = l               

    # Print best scoring starting station
    print(f" -" * 20)  
    g = Graph(num_stations, top_station)
    print("Best schedule: ")
    print(f"Top score: {top_score}")  
    print()        

    with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
        next(f)       
        for i in range(num_connections):
            connection_str = f.readline()
            connection = connection_str.split(",")
        
            station_1 = connection[0]
            station_2 = connection[1]            
            
            for j in range(num_stations):
                if stations[j].station_name == station_1:
                    save_station_1 = j                    
                if stations[j].station_name == station_2:
                    save_station_2 = j
                    
            g.addEdge(save_station_1, save_station_2)
            g.addEdge(save_station_2, save_station_1)
            
    g.printEulerTour()	

    # Calculate average results algorithm          
    average_score = average_score / num_stations   
    average_time = average_time / num_stations
    
    # Print average results algorithm
    print()
    print(f" -" * 20) 
    print(f"Average score: {round(average_score, 2)}")
    print(f"Average time: {round(average_time, 2)}")

elif style == "greedy":
    greedy()


else:
    print("Please give an existing style.\nStyles:\n- normal\n- single\n- max")
        