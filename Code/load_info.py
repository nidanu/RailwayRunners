#!/usr/bin/env python 
"""
Loads info from .csv file into Station classes.
"""
from Code.Classes.station import Station
from Code.Classes.station_postman import Station_Postman
from Code.Classes.station import Station
from typing import List

def create_list_of_stations(station_file: str) -> List:
    """
    Opens .csv file with the stations and initiates them into the Station class.
    
    Returns a list of all the stations and the number of stations in the case.
    """

    # Create list for all stations
    stations = []       

    # Count number of stations
    with open(station_file, "r") as f:
        next(f)
        num_stations = len(f.readlines())  

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
            
            new_station = Station(i, station_name, station_y, station_x)
            stations.append(new_station)   

    return stations, num_stations       

def postman_station(station_file: str, connection_file: str):
    """
    Opens .csv file with the stations and initiates them into the Station_Postman class.
    
    Returns a list of all the stations and the class.
    """
    # Create list for all stations
    stations = []       
  
    # Count number of stations
    with open(station_file, "r") as f:
        next(f)
        num_stations = len(f.readlines())  
    
    # Count number of connections
    with open(connection_file, "r") as f:
        next(f)   
        num_connections = len(f.readlines())

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
            
            new_station = Station_Postman(station_name)
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
                    stations[i].add_connection(station_2, int(traveltime))
                if stations[i].station_name == station_2:
                    stations[i].add_connection(station_1, int(traveltime))
    
    return stations, Station_Postman

def create_station_connections(station_file: str, connection_file: str, stations: List[Station]) -> int:
    """
    Opens .csv file with the connections and initiates them into the Station class.
    
    Returns the number of connections in the case.
    """
    # Count number of stations    
    with open(station_file, "r") as f:
        next(f)
        num_stations = len(f.readlines())  

    # Count number of connections
    with open(connection_file, "r") as f:
        next(f)       
        num_connections = len(f.readlines())  

    # Load connections into Station objects
    with open(connection_file, "r") as f:
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
                    
            traveltime_str = connection[2].split('\n')        
            traveltime = int(float(traveltime_str[0]))

            for i in range(num_stations):
                if stations[i].station_name == station_1:
                    stations[i].add_connection(str(save_station_2), int(traveltime))
                if stations[i].station_name == station_2:
                    stations[i].add_connection(str(save_station_1), int(traveltime))  
    
    return num_connections