import random

from station import Station
from train import Train

# Create list with all stations
stations = []

# Count number of stations
with open("StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())
    #print(f"Number of stations: {num_stations}")

# Count number of connections
with open("ConnectiesHolland.csv", "r") as f:
    next(f)   
    num_connections = len(f.readlines())
    #print(f"Number of connections: {num_connections}")

#print()    

# Create list of Station objects
with open("StationsHolland.csv", "r") as f:
    next(f)

    for i in range(num_stations):
        station_info = f.readline().split(',')
        station_info = station_info
        station_name = station_info[0]
        
        station_y = float(station_info[1])
        station_x_str = station_info[2].split('\n')
        station_x = float(station_x_str[0]) 
        
        new_station = Station(station_name, station_y, station_x)
        stations.append(new_station)

# Load connections into Station objects
with open("ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(num_connections):    
        connection_str = f.readline()
        connection = connection_str.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime_str = connection[2].split('\n')
        traveltime = int(traveltime_str[0])

        for i in range(num_stations):
            if stations[i].station_name == station_1:
                stations[i].add_connection(station_2, traveltime)
            if stations[i].station_name == station_2:
                stations[i].add_connection(station_1, traveltime)   

    # Print all station connections            
    #for i in range(num_stations):
        #print(stations[i].station_name, end=": ")
        #print(stations[i].connections)

#print()

# Create Train object with random start station
train = Train((stations[random.randint(0, len(stations) - 1)]))
print(f"Train name: {train.train_name.station_name}")
print()

# Move train till time is up
while train.travel_time < 120:

    # Pick random next station from station connections
    next_station_name = train.choose_next_station()
    next_station_List = [station for station in stations if station.station_name == next_station_name]
    next_station = next_station_List[0]
    
    #print(f"Next destination: {next_station.station_name}")
    
    # Update total travel time of train
    train.update_travel_time(next_station)
    #print(f"Total travel time: {train.travel_time}")

    # Add next station to travel history and move towards it
    train.add_destination_to_history(next_station)
    #print()

# Print route
for destinations in train.destination_history:
    print(f"Visited station: {destinations}")

     
