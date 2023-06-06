from station import Station
from train import Train

stations = []

# Create list of Station objects
with open("StationsHolland.csv", "r") as f:
    next(f)

    for i in range(22):
        station_info = f.readline().split(',')
        station_info = station_info
        station_name = station_info[0]
        
        station_y = station_info [1]
        station_x = station_info[2].split('\n')
        station_x = station_x[0] 
        
        new_station = Station(station_name, station_y, station_x)
        stations.append(new_station)

# Load connections into Station objects
with open("ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(28):    
        connection = f.readline()
        connection = connection.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime = connection[2].split('\n')
        traveltime = int(traveltime[0])

        for i in range(22):
            if stations[i].station_name == station_1:
                stations[i].connections[station_2]=traveltime
            if stations[i].station_name == station_2:
                stations[i].connections[station_1]=traveltime     
                
    for i in range(22):
        print(stations[i].connections)
print()

# Create Train object
train = Train(stations[0].station_name)
print(train.train_name)

# Add destination Den Helder
try:
    train.add_destination(stations[10].station_name, stations[0].connections[(stations[10].station_name)])
    print(f"Added: {stations[10].station_name}")
except:
    print("Connection not available")    
print(train.travel_time)
print(train.destination_history)
print()

# Add destination Dordrecht
try:
    train.add_destination(stations[11].station_name, stations[0].connections[(stations[11].station_name)])
    print(f"Added: {stations[11].station_name}")
except:
    print("Connection not available")    
print(train.travel_time)
print(train.destination_history)