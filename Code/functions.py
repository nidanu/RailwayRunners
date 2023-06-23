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

"""
FUnctions for random algorithm  
"""

def determine_max_routes(num_stations):
    if num_stations == 22:
        return 7
    elif num_stations == 61:
        return 20
    else:
        return None 

def check_progress(runs, total_runs, progress):
    if runs % (total_runs // 10) == 0:
        print(f"{progress}%")
        progress += 10
    return progress

def get_next_station(train, stations):
    next_station_number = train.choose_next_station()
    next_station_List = [station for station in stations if station.station_number == next_station_number]
    next_station = next_station_List[0]
    return next_station

def check_and_append_visited(next_station, visited):
    if next_station.station_name not in visited:
        visited.append(next_station.station_name)
    return visited

def check_and_append_driven(cur_station, next_station, temp_list_connections, driven):
    one_way = [cur_station.station_name, next_station.station_name]
    if one_way in temp_list_connections:
        temp_list_connections.remove(one_way)
        driven.append(one_way)
    
    other_way = [next_station.station_name, cur_station.station_name]
    if other_way in temp_list_connections:
        temp_list_connections.remove(other_way)
        driven.append(other_way)
    return driven

def save(train, travel_times, routes):
    travel_times.append(train.travel_time)
    routes.append(train.destination_history)
    return travel_times, routes

def reset(train):
    train.travel_time_zero()
    train.empty_destination_history()
    return train

def calculate_score(list_connections, temp_list_connections, routes, travel_times):
    n_connections_driven = len(list_connections) - len(temp_list_connections)
    p = n_connections_driven / len(list_connections)
    T = len(routes)
    Min = sum(travel_times)
    K = p * 10000 - (T * 100 + Min)
    return K

