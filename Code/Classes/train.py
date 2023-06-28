#!/usr/bin/env python # 
"""
Configuration of a train class that travels between stations.
"""
import random
from Code.Classes.station import Station
from typing import List

class Train:
    """
    Train class representing a moving train. 

    Attributes:
    - - - - - - - 
    - train_name: str
        the name of the station it started at
    - current_station: str
        the name of the station it is currently located at
    - travel_time: int
        total time the train has travelled
    - destination_history: List[str]
        a list of stations the train has visited
    """
    def __init__(self, start_station: Station) -> None:
        self.train_name = start_station
        self.current_station = start_station
        self.travel_time = 0
        self.destination_history: List[str] = [start_station.station_name]     

    def add_destination_to_history(self, next_station: Station) -> None:
        """
        Once the train has visited a station, the station is added to its past visited stations.
        """
        self.destination_history.append(next_station.station_name)
        self.current_station = next_station  
       
    def choose_next_station(self) -> str:
        """"
        Selects a random station from a list of possible stations. This becomes the new
        end station. Returns the station name.
        """
        destination_list = list(self.current_station.connections.keys())   
        next_station = (destination_list[random.randint(0, len(destination_list) - 1)])                 
        return next_station
    
    def update_travel_time(self, next_station: Station) -> None:
        """
        The train keeps track of how long it has been running. After traversing a connection
        its travel time is updated.
        """
        self.travel_time += self.current_station.connections[str(next_station.station_number)]
        
    def travel_time_zero(self) -> None:
        """
        Resets the train's travel time to 0.
        """
        self.travel_time = 0
    
    def empty_destination_history(self) -> None:
        """
        Resets the train's history of visited station to the station it is currently located at.
        """
        self.destination_history = [self.current_station.station_name]     
                