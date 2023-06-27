#!/usr/bin/env python 
"""
File to determine case for algorithms.
"""
from typing import List, Tuple
from Classes.station import Station
from load_info import create_list_of_stations, create_station_connections

def choose_case() -> Tuple[int, int, str, str, List['Station'], List[Tuple[str, str]], int, int, int]:
    """
    Asks user to choose which case they want to run the algorithms on: Holland or the Netherlands.
    Returns necessary variables to run the algorithms in main.py.
    """
    choose_case = input("Within Holland or the Netherlands? Select 'H' or 'N'. ")
    if choose_case.lower() == 'h':
        file_stations = "../Cases/Holland/StationsHolland.csv"
        file_connections = "../Cases/Holland/ConnectiesHolland.csv"
        max_time = 120
        max_trajectories = 7
    elif choose_case.lower() == 'n':
        file_stations = "../Cases/Netherlands/StationsNationaal.csv"
        file_connections = "../Cases/Netherlands/ConnectiesNationaal.csv"
        max_time = 180
        max_trajectories = 22
    else:
        print("Invalid input.")

    with open(file_connections, "r") as f:
        next(f)
        list_connections = []
        list_connection_lengths = []
        for connection in f.readlines():
            cur_connection = connection.split(",")
            clean_connection = cur_connection[0:2]
            list_connections.append(clean_connection)            
            list_connection_lengths.append(float(cur_connection[2]))
        min_time = sum(list_connection_lengths)

    stations, num_stations = create_list_of_stations(file_stations)
    num_connections = create_station_connections(file_stations, file_connections, stations)

    return num_connections, num_stations, file_stations, file_connections, stations, list_connections, min_time, max_time, max_trajectories