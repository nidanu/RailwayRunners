import random
import sys
sys.path.append('..')
from Classes.train import Train
from Code.load_info import create_list_of_stations, create_station_connections 

def greedy():
    progress = 0
    sum_scores = 0
    top_score = 0
     
    num_runs = int(input("How many runs? "))
   
    for i in range(num_runs):
        # Progress printer 
        if i == 1 or (i % (num_runs/10) == 0):
            print(f"{progress}%")
            progress += 10        
        
        # Create list with all stations + connections
        stations = create_list_of_stations("../Cases/Holland/StationsHolland.csv")
        create_station_connections("../Cases/Holland/StationsHolland.csv", "../Cases/Holland/ConnectiesHolland.csv", stations)

        # Count number of stations
        with open("../Cases/Holland/StationsHolland.csv", "r") as f:
            next(f)
            num_stations = len(f.readlines())  

        # Count number of connections
            with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
                next(f)       
                num_connections = len(f.readlines())   

        # Creates list of connections 
        with open("../Cases/Holland/ConnectiesHolland.csv", "r") as f:
            next(f)
            list_connections = []    
            for connection in f.readlines():
                cur_connection = connection.split(",")
                clean_connection = cur_connection[0:2]
                list_connections.append(clean_connection)    
        
        # Count number of connections
        num_connections = len(list_connections)

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
        while (len(list_connections) > 0) and train_count < 8: 

            # Create Train object with random start station, remove station number from list of possible starting stations
            list_number = random.randint(0, len(list_station_numbers) - 1)
            next_station_number = list_station_numbers[list_number]         
            list_station_numbers.pop(list_number)
            train = Train(stations[next_station_number])
            
            # Set current station to starting station train
            current_station_number = train.train_name.station_number
            current_station = stations[current_station_number]

            # Save train information to network list
            network.append(" -" * 20)
            network.append(f"Route {train_count}")
            
            # Add destinations to Train object while travel time is below 120 minutes
            while train.travel_time < 120:

                # Create list of stations sorted by distance from current station
                station_connections = stations[current_station_number].connections    
                sorted_station_connections = (sorted(station_connections.items(), key=lambda x: x[1]))
                num_station_connections = len(sorted_station_connections)

                # Select next station that has not been visited yet by train, closest in range
                for i in range(num_station_connections):                
                    if stations[sorted_station_connections[0][0]].station_name in train.destination_history:
                        sorted_station_connections.pop(0)           
                    else:            
                        closest_connection = stations[sorted_station_connections[0][0]].station_number           
                        break    
                    if len(sorted_station_connections) == 0:                
                        break              
                
                # End route if train reaches dead end
                if closest_connection not in train.current_station.connections:       
                    break
                
                # End route if travel_time goes above 120 minutes with next destination, else move to next station                    
                if (train.travel_time + train.current_station.connections[closest_connection]) > 120:      
                    break
                else:                    
                    for i in range(len(list_connections)):               
                        # Delete visited connection from list of connections
                        if list_connections[i][0] == current_station.station_name and list_connections[i][1] == stations[closest_connection].station_name:
                            current_connection = i                    
                            list_connections.pop(current_connection)
                            break
                        elif list_connections[i][0] == stations[closest_connection].station_name and list_connections[i][1] == current_station.station_name:
                            current_connection = i                   
                            list_connections.pop(current_connection)
                            break

                    # Update total travel time of train
                    train.update_travel_time(stations[closest_connection])                            

                    # Add next station to travel history and move towards it
                    train.add_destination_to_history(stations[closest_connection])      

                    # Update current station
                    current_station = stations[closest_connection]
                    current_station_number = stations[closest_connection].station_number               
           
            # Add train travel time to total, and save train network to list of network information
            total_travel_time += train.travel_time              
            network += train.destination_history

            # Move to new train
            train_count += 1

        # Calculate fraction of visited connections
        p = (len(list_connections) / num_connections)
        p = 1 - p

        # Calculate number of trains in network
        T = train_count - 1    
        
        # Set total travel time of all trains in network
        Min = total_travel_time

        # Calculate the quality score for network, and add to sum of all network scores
        final_score = p*10000 - (T*100 + Min)
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