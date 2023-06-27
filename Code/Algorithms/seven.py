from Classes.bridges import Graph

def seven_bridges(num_stations, num_connections, stations, list_connections, min_time, file_connections, max_time): 
    # Create variables for score calculations
    top_score = 0 
    average_score = 0 
    average_time = 0  

    # Create network starting from each available station and calculate network score
    for l in range(num_stations):  
        # Create empty Graph and print starting station route              
        g = Graph(num_stations, l, stations, num_stations, max_time, list_connections, file_connections) 
        print(f" -" * 20)             
        print(f"Starting station: {stations[g.starting_station].station_name} \n")

        # Load all connections into Graph
        with open(file_connections, "r") as f:
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
                    
                g.addEdge(save_station_1, save_station_2)
                g.addEdge(save_station_2, save_station_1)

        # Print calculated Graph, score and network total time    
        
        g.printEulerTour()	
        print()
        print(f"Score: {round(g.final_score, 2)}")
        print(f"Total time: {g.total_time_network}")   

        # Add score and time to variables to calculate overall average
        average_score += g.final_score
        average_time += g.total_time_network
        
        # Compare all scores for highest result, and save station number of best station
        if g.final_score > top_score:
            top_score = g.final_score
            top_station = l               

    # Print best scoring starting station
    print(f" -" * 20)  
    g = Graph(num_stations, top_station, stations, num_stations, max_time, list_connections, file_connections)
    print("Best schedule: ")
    print(f"Top score: {top_score}")  
    print()        

    with open(file_connections, "r") as f:
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
                    
            g.addEdge(save_station_1, save_station_2)
            g.addEdge(save_station_2, save_station_1)
            
    g.printEulerTour()	

    # Calculate average results algorithm          
    average_score = average_score / num_stations   
    average_time = average_time / num_stations
    
    # Print average results algorithm
    print()
    print(f" -" * 20) 
    print(f"Average score: {round(average_score, 2)}")
    print(f"Average time: {round(average_time, 2)}")
