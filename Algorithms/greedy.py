import random
import sys
sys.path.append('..')

from Classes.station import Station
from Classes.train import Train
from Code.load_info import create_list_of_stations, create_station_connections 

from typing import List


def greedy(num_stations: int, num_connections: int, stations: List[Station], list_connections: List[List[int]], min_time: int, max_time: int, max_trajectories: int) -> None:
    progress = 0
    sum_scores = 0.0
    top_score = 0.0  
        
    list_connections_copy = list_connections

    num_runs = int(input("How many runs? "))
   
    for i in range(num_runs):
        # Progress printer 
        if i == 1 or (i % (num_runs/10) == 0):
            print(f"{progress}%")
            progress += 10                     

        # Set up copy of list of connections
        list_connections = list_connections_copy

        # Set train number to 1, and total travel time to 0          
        train_count = 1      
        total_travel_time = 0
        
        # Create list of all station numbers
        list_station_numbers = []
        for i in range(num_stations):
            list_station_numbers.append(i)

        # Create list to save network each run    
        network = []

        # Add a maximum of 7 trains to network while connections are unvisited 
        while (len(list_connections) > 0) and train_count <= max_trajectories: 

            # Create Train object with random start station, remove station number from list of possible starting stations        
            if len(list_station_numbers) == 0:
                break
            list_number = random.randint(0, len(list_station_numbers) - 1)             
            next_station_number = list_station_numbers[list_number]         
            list_station_numbers.pop(list_number)
            train = Train(stations[next_station_number])
            
            # Set current station to starting station train
            current_station_number = train.train_name.station_number
            current_station = stations[current_station_number]

            # Save grid to network list
            network.append(" -" * 20)           
            
            # Add destinations to Train object while travel time is below 120 minutes
            while train.travel_time < max_time:

                # Create list of stations sorted by distance from current station
                station_connections = stations[current_station_number].connections    
                sorted_station_connections = (sorted(station_connections.items(), key=lambda x: x[1]))
                num_station_connections = len(sorted_station_connections)
                
                # Select next station that has not been visited yet by train, closest in range
                for i in range(num_station_connections):                      
                    if str(stations[int(sorted_station_connections[0][0])].station_name) in (train.destination_history):
                        sorted_station_connections.pop(0)           
                    else:            
                        closest_connection = stations[int(sorted_station_connections[0][0])].station_number           
                        break    
                    if len(sorted_station_connections) == 0:                
                        break              
                
                # End route if train reaches dead end                
                if str(closest_connection) not in train.current_station.connections:       
                    break
                
                # End route if travel_time goes above 120/360 minutes with next destination, else move to next station                    
                if (train.travel_time + train.current_station.connections[str(closest_connection)]) > max_time:      
                    break
                else:                    
                    for i in range(len(list_connections)):               
                        # Delete visited connection from list of connections
                        if str(list_connections[i][0]) == current_station.station_name and str(list_connections[i][1]) == stations[closest_connection].station_name:
                            current_connection = i                    
                            list_connections.pop(current_connection)
                            break
                        elif str(list_connections[i][0]) == stations[closest_connection].station_name and str(list_connections[i][1]) == current_station.station_name:
                            current_connection = i                   
                            list_connections.pop(current_connection)
                            break

                    # Update total travel time of train
                    train.update_travel_time(stations[closest_connection])                            

                    # Add next station to travel history and move towards it
                    train.add_destination_to_history((stations[closest_connection]))      
                    
                    # Update current station                    
                    for i in range(len(list_station_numbers) - 1):               
                        if list_station_numbers[i] == current_station_number and len(list_station_numbers) > 0:
                            list_station_numbers.pop(i)

                    current_station = stations[closest_connection]
                    current_station_number = stations[closest_connection].station_number               
           
            # Add train travel time to total, and save train network to list of network information
            total_travel_time += train.travel_time              
            network += train.destination_history

            # Print route time and move to new train
            network.append(f"ROUTE {train_count}: {train.travel_time} minutes")
            train_count += 1

        # Calculate fraction of visited connections
        p = (len(list_connections) / num_connections)
        p = 1 - p

        # Calculate number of trains in network
        T = train_count - 1    
        
        # Set total travel time of all trains in network
        Min = total_travel_time

        # Calculate the quality score for network, and add to sum of all network scores
        final_score = p*10000 - ((T*100) + Min)
        sum_scores += final_score
               
        # Save best score and network
        if final_score > top_score:
            top_score = final_score
            top_route = network  

    # Calculate average network quality score of all runs
    average_score = sum_scores / num_runs 
   
    # Print information about all runs, and high score network
    print(f"Average score: {round(average_score, 0)}")         
    print(f"Top score: {round(top_score, 0)}")  
    print()
    print("Best network: ")
    for i in range(len(top_route)):
        print(top_route[i])