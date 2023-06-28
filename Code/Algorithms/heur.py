import random
import time
import matplotlib.pyplot as plt
from scipy import stats
from Code.Classes.train import Train
from Code.functions import *


def heur(num_stations, num_connections, stations, list_connections, min_time):
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

    #----------------------------------------------------------------------------------------------------
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
    # Shapiro-Wilk Test
    shapiro_test = stats.shapiro(scores)
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}")
    print(f"P-value: {shapiro_test.pvalue}")
    


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
