from Classes.station import Station
from typing import List


def create_list_of_stations(filename_stations) -> List:    

    # Create list for all stations
    stations = []       

    # Count number of stations
    with open(filename_stations, "r") as f:
        next(f)
        num_stations = len(f.readlines())  

    # Create list of Station objects
    with open(filename_stations, "r") as f:
        next(f)

        for i in range(num_stations):
            station_info = f.readline().split(',')
            station_info = station_info
            station_name = station_info[0]
            
            station_y = float(station_info[1])
            station_x_str = station_info[2].split('\n')
            station_x = float(station_x_str[0]) 
            
            new_station = Station(i, station_name, station_y, station_x)
            stations.append(new_station)     
    return stations        
  

def create_station_connections(filename_stations, filename_connections, stations: List[Station]) -> None:

    # Count number of stations
    with open(filename_stations, "r") as f:
        next(f)
        num_stations = len(f.readlines())  

    # Count number of connections
    with open(filename_connections, "r") as f:
        next(f)       
        num_connections = len(f.readlines())  

    # Load connections into Station objects
    with open(filename_connections, "r") as f:
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
                    
            traveltime_str = connection[2].split('\n')        
            traveltime = int(float(traveltime_str[0]))

            for i in range(num_stations):
                if stations[i].station_name == station_1:
                    stations[i].add_connection(save_station_2, traveltime)
                if stations[i].station_name == station_2:
                    stations[i].add_connection(save_station_1, traveltime)  
   
