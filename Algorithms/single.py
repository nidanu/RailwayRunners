import random
import time
import sys 
sys.path.append('..')
from Classes.train import Train
from Code.functions import *

def single(num_stations, num_connections, stations, list_connections, min_time):
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