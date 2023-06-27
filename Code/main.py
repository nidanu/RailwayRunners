#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""
from Algorithms.greedy import greedy
from Algorithms.seven import seven_bridges 
from Algorithms.postman import Postman
from Algorithms.heur import heur
from Algorithms.normal import normal
from Algorithms.single import single
from functions import *
from load_info import postman_station
from choose_case import choose_case

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
        runs = input("How many runs? Enter an integer. ")
        if int(runs) > 0:
            stations, Station_Postman = postman_station(file_stations, file_connections)
            Postman.postman_algorithm(max_time, max_trajectories, int(runs))
        else:
            print("Enter valid input.")

    else:
        print("Please give an existing style.\nStyles:\n- normal\n- single\n- max\n- heur\n- greedy\n- 7\n- postman")

main()