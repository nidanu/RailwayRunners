#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""
from Code.Algorithms.greedy import greedy
from Code.Algorithms.seven import seven_bridges 
from Code.Algorithms.postman_tour import postman_algorithm
from Code.Algorithms.heur import heur
from Code.Algorithms.normal import normal
from Code.Algorithms.single import single
from Code.functions import *
from Code.load_info import postman_station
from Code.choose_case import choose_case
from Visualisation.network import nx_network

def main():
    num_connections, num_stations, file_stations, file_connections, stations, list_connections, min_time, max_time, max_trajectories = choose_case()
    
    # Ask for test input
    print("Styles:\n- normal\n- single\n- max\n- heur\n- greedy\n- 7\n- postman")
    style = input("What style of test? ")
    
    # Contains all styles of tests 
    if style.lower() == "max":
        # find in main save
        pass

    elif style.lower() == "single":
        single(num_stations, num_connections, stations, list_connections, min_time)

    # Runs random for x amount of times    
    elif style.lower() == "normal":
        normal(num_stations, num_connections, stations, list_connections, min_time)

    elif style == "heur":
        heur(num_stations, num_connections, stations, list_connections, min_time)
        
    elif style == "7":
        seven_bridges(num_stations, num_connections, stations, list_connections, min_time, file_connections, max_time)

    elif style == "greedy":
        greedy(num_stations, num_connections, stations, list_connections, min_time, max_time, max_trajectories)

    elif style == "postman":
        stations, Station_Postman = postman_station(file_stations, file_connections)
        postman_algorithm(max_time, max_trajectories)

    else:
        print("Please give an existing style.\nStyles:\n- normal\n- single\n- max\n- heur\n- greedy\n- 7\n- postman")

def visuals():
    num_connections, num_stations, file_stations, file_connections, stations, list_connections, min_time, max_time, max_trajectories = choose_case()
    nx_network(stations)

main()