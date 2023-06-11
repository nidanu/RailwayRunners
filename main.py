#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""

import random

from Classes.station import Station
from Classes.train import Train
from graph import *

# Create list with all stations
stations = []

# Count number of stations
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())
    #print(f"Number of stations: {num_stations}")

# Count number of connections
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)   
    num_connections = len(f.readlines())
    #print(f"Number of connections: {num_connections}")

#print()    

# Create list of Station objects
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)

    for i in range(num_stations):
        station_info = f.readline().split(',')
        station_info = station_info
        station_name = station_info[0]
        
        station_y = float(station_info[1])
        station_x_str = station_info[2].split('\n')
        station_x = float(station_x_str[0]) 
        
        new_station = Station(station_name, station_y, station_x)
        stations.append(new_station)

# Load connections into Station objects
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(num_connections):    
        connection_str = f.readline()
        connection = connection_str.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime_str = connection[2].split('\n')
        traveltime = int(traveltime_str[0])

        for i in range(num_stations):
            if stations[i].station_name == station_1:
                stations[i].add_connection(station_2, traveltime)
            if stations[i].station_name == station_2:
                stations[i].add_connection(station_1, traveltime)   

    # Print all station connections            
    #for i in range(num_stations):
        #print(stations[i].station_name, end=": ")
        #print(stations[i].connections)

#print()

# Create Train object with random start station
train = Train((stations[random.randint(0, len(stations) - 1)]))
print(f"Train name: {train.train_name.station_name}")
print()

# Move train till time is up
n_routes = 1
travel_times = []
routes = []
visited = [train.current_station.station_name]
while n_routes <= 7:
    while train.travel_time <= 120:

        # Pick random next station from station connections
        next_station_name = train.choose_next_station()
        next_station_List = [station for station in stations if station.station_name == next_station_name]
        next_station = next_station_List[0]
        
        #print(f"Next destination: {next_station.station_name}")
        if (train.travel_time + train.current_station.connections[next_station.station_name]) > 120:
            break
        else:
            # Update total travel time of train
            train.update_travel_time(next_station)
            #print(f"Total travel time: {train.travel_time}")

            # Add next station to travel history and move towards it
            train.add_destination_to_history(next_station)
            #print()
            
            if next_station.station_name not in visited:
                visited.append(next_station.station_name)
        
    travel_times.append(train.travel_time)
    routes.append(train.destination_history)
    train.travel_time_zero()
    train.empty_destination_history()
    n_routes += 1

# Print route
print("=============================================")
for i in range(len(routes)):
    print(f"Route: {i + 1} ----------------")
    for destinations in routes[i]:
        print(f"{destinations}") #Visited station:
    print(f"Total time route: {travel_times[i]}")

print(f"\nTotal time: {sum(travel_times)}\n")

print("Visited:")
for been_there in visited:
    print(been_there)
print()
print(f"Total visited stations: {len(visited)}")

# Function from graph.py, creates network graph of the stations
# mapping()
     
