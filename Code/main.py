#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""

import random
import sys 
sys.path.append('..')

from Algorithms.bridges import Graph  
from Classes.station import Station
from Classes.train import Train
from Code.functions import create_list_of_stations, create_station_connections
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

# Ask for test input
print("Styles:\n- normal\n- single\n- max\n- 7")
style = input("What style of test? ")
print()

# Contains all styles of tests 
if style.lower() == "max":

    # Set variables for big loop
    runs = 1
    scores_and_routes = [] 
    progress = 0
    max_routes = int(input("How many routes? "))
    total_runs = int(input("How many runs? "))

    # Runs question under restrictions n times until completion
    while runs <= total_runs:        

        # Progress printer 
        if runs == 1 or (runs % (total_runs/10) == 0):
            print(f"{progress}%")
            progress += 10
        
        visited: List[str] = []
        number_of_stations = len(stations)
        
        # End if all stations are visited, else create new route 
        while len(visited) != number_of_stations:

            # Create Train object with random start station
            train = Train((stations[random.randint(0, len(stations) - 1)]))
            
            # Set loop variables
            n_routes = 1
            travel_times = []
            routes = []
            visited = [train.current_station.station_name]

            # Move train until max routes 
            while n_routes <= max_routes:

                # Move train till time is up
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
                        
                        # adds station to visited if aplicable 
                        if next_station.station_name not in visited:
                            visited.append(next_station.station_name)
                    
                # Save and reset
                travel_times.append(train.travel_time)
                routes.append(train.destination_history)
                train.travel_time_zero()
                train.empty_destination_history()
                n_routes += 1
        
        # Calculate and store scores
        p = len(visited)/len(stations)
        T = max_routes
        Min = sum(travel_times)
        K = p*10000 - (T*100 + Min)
        scores_and_routes.append([K, routes, travel_times]) 
        
        runs += 1

    # Sorts and separates output
    scores_and_routes.sort(key=lambda x: x[0])
    scores = [] 
    for score_and_route in scores_and_routes:
        scores.append(score_and_route[0])

    # Print max rout with travel time
    top_route = scores_and_routes[-1][1]
    top_travel_time = scores_and_routes[-1][2]
    top_travel_times = []
    
    print()
    print(" =" * 40)
    print()

    for i in range(len(top_route)):
        print(f"Route: {i + 1}" + " -" * 20)
        for destinations in top_route[i]:
            print(f"{destinations}")  # Visited station:
        print(f"Total time route: {top_travel_time[i]}\n")
        top_travel_times.append(top_travel_time[i])

    # Prints top scores
    top_scores = scores[-3:]
    print("Top scores:")
    for top_score in top_scores:
        print(top_score)
    print()

    # Prints low scores 
    low_scores = scores[:3]
    print("Low scores:")
    for low_score in low_scores:
        print(low_score)
    print()

    # Prints avarage and max scores
    avg_score = sum(scores)/len(scores)
    top_score = max(scores)
    print(f"Avg score: {avg_score}")
    print(f"Top score: {top_score}")
    print(f"Top time: {sum(top_travel_times)}")
    print(f"Routes: {max_routes}")
    print(f"Runs: {total_runs}")
    
elif style.lower() == "single":
    # Create Train object with random start station
    train = Train((stations[random.randint(0, len(stations) - 1)]))    

    # Move train till all stations are visited or out of routes or route travel_time >= 120
    n_routes = 1
    travel_times = []
    routes = []
    visited = [train.current_station.station_name]
    while (n_routes <= 7) and (len(visited) <= len(stations)):
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
        
        # Save route specific information
        travel_times.append(train.travel_time)
        routes.append(train.destination_history)
        train.travel_time_zero()
        train.empty_destination_history()
        n_routes += 1        

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

    # Print list of all NOT visited stations
    print("Not visited:")
    for station_name in not_visited:
        print(station_name)
    print()

    # Print travel statistics
    print(f"Visited: {len(visited)}")
    print(f"NOT visited: {len(not_visited)}")
    print()
    
    # Calculate score
    p = len(visited)/len(stations)
    T = n_routes - 1
    Min = sum(travel_times)
    K = p*10000 - (T*100 + Min)
    
    # Print statistic
    print(f"Routes: {T}")
    print(f"Total time: {sum(travel_times)}")
    print(f"Score: {K}")
    
elif style.lower() == "normal":
    # Set variables for big loop
    scores_and_routes = [] 
    progress = 0
    total_runs = int(input("How many runs? "))
    runs = 0
    max_routes = 7
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
        while (n_routes <= max_routes) and (len(visited) <= len(stations)):
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
            
            # Save and reset
            travel_times.append(train.travel_time)
            routes.append(train.destination_history)
            train.travel_time_zero()
            train.empty_destination_history()
            n_routes += 1

        # Calculate and store scores
        p = len(visited)/len(stations)
        T = len(routes)
        Min = sum(travel_times)
        K = p*10000 - (T*100 + Min)
        scores_and_routes.append([K, routes, travel_times]) 
            
        runs += 1

    # Sorts and separates output
    scores_and_routes.sort(key=lambda x: x[0])
    scores = [] 
    for score_and_route in scores_and_routes:
        scores.append(score_and_route[0])

    # Print max route with travel time
    top_route = scores_and_routes[-1][1]
    top_travel_time = scores_and_routes[-1][2]
    top_travel_times = []

    print()
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
    top_scores = scores[-3:]
    print("Top scores:")
    for top_score in top_scores:
        print(top_score)
    print()

    # Prints low scores 
    low_scores = scores[:3]
    print("Low scores:")
    for low_score in low_scores:
        print(low_score)
    print()

    # Prints avarage and max scores
    avg_score = sum(scores)/len(scores)
    top_score = max(scores)
    print(f"Avg score: {avg_score}")
    print(f"Top score: {top_score}")
    print(f"Top time: {sum(top_travel_times)}")
    print(f"Top Routes: {len(top_route)}")
    print(f"Max routes: {max_routes}")
    print(f"Runs: {total_runs}")

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
        with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
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

    with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
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

else:
    print("Please give an existing style.\nStyles:\n- normal\n- single\n- max")
        