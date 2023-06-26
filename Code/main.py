#!/usr/bin/env python # 
"""
Runs simulation of train travelling through network map of all connections.
"""

import sys 
sys.path.append('..')
from Classes.bridges import Graph  
from Algorithms.random_dijkstra import *
from Algorithms.greedy import greedy
from Algorithms.seven import seven_bridges 
from Algorithms.postman import *
from Algorithms.heur import heur
from Algorithms.normal import normal
from Algorithms.single import single
from Code.functions import *
from load_info import *

choose_case = input("Within Holland or the Netherlands? Select 'H' or 'N'. ")
if choose_case.lower() == 'h':
    file_stations = "../Cases/Holland/StationsHolland.csv"
    file_connections = "../Cases/Holland/ConnectiesHolland.csv"
    max_time = 120
    max_trajectories = 7
elif choose_case.lower() == 'n':
    file_stations = "../Cases/Netherlands/StationsNationaal.csv"
    file_connections = "../Cases/Netherlands/ConnectiesNationaal.csv"
    max_time = 360
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

# Ask for test input
print("Styles:\n- normal\n- single\n- max\n- heur\n- greedy\n- 7\n- postman\n- random dijkstra")
style = input("What style of test? ")
stations, num_stations = create_list_of_stations(file_stations)
num_connections = create_station_connections(file_stations, file_connections, stations) 

# Contains all styles of tests 
if style.lower() == "max":
    # find in main save
    pass

elif style.lower() == "single":
    single.single(num_stations, num_connections, stations, list_connections, min_time)

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

elif style == "random dijkstra":
    runs = input("How many runs? Enter an integer. ")
    if int(runs) > 0:
        maximum, minimum, average = Quick_dijkstra.random_dijkstra(int(runs), max_time)
        print(f"The maximum score for {runs} runs is {maximum}, the minimum is {minimum}, and the mean is {average}.")
    else:
        print("Enter valid input.")

else:
    print("Please give an existing style.\nStyles:\n- normal\n- single\n- max")
        