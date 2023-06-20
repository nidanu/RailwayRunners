#!/usr/bin/env python 
"""
Loads info from .csv file into Station classes.
"""
import sys
sys.path.append("..")
from Classes.station_postman import *

def load(station_file: str, connection_file: str):
    # Create list with all stations
    stations = []

    # Count number of stations
    with open(station_file, "r") as f:
        next(f)
        num_stations = len(f.readlines())
        #print(f"Number of stations: {num_stations}")

    # Count number of connections
    with open(connection_file, "r") as f:
        next(f)   
        num_connections = len(f.readlines())
        #print(f"Number of connections: {num_connections}")

    #print()    

    # Create list of Station objects
    with open(station_file, "r") as f:
        next(f)

        for i in range(num_stations):
            station_info = f.readline().split(',')
            station_info = station_info
            station_name = station_info[0]
            
            station_y = float(station_info[1])
            station_x_str = station_info[2].split('\n')
            station_x = float(station_x_str[0]) 
            
            new_station = Station_Postman(station_name, station_y, station_x)
            stations.append(new_station)

    # Load connections into Station objects
    with open(connection_file, "r") as f:
        next(f)
        for i in range(num_connections):    
            connection_str = f.readline()
            connection = connection_str.split(",")
            
            station_1 = connection[0]
            station_2 = connection[1]
            traveltime_str = connection[2].split('\n')
            traveltime = float(traveltime_str[0])

            for i in range(num_stations):
                if stations[i].station_name == station_1:
                    stations[i].add_connection(station_2, traveltime)
                if stations[i].station_name == station_2:
                    stations[i].add_connection(station_1, traveltime)   

        # Print all station connections            
        #for i in range(num_stations):
            #print(stations[i].station_name, end=": ")
            #print(stations[i].connections)

    return stations, Station_Postman, num_connections