#!/usr/bin/env python # 
"""
Configuration of a train class that travels between stations.
"""

import random

from Classes.station import Station
from typing import List


class Train:
    def __init__(self, start_station: Station) -> None:
        self.train_name = start_station
        self.current_station = start_station
        self.travel_time = 0
        self.destination_history: List[str] = [start_station.station_name]     

    def add_destination_to_history(self, next_station: Station) -> None:
        self.destination_history.append(next_station.station_name)
        self.current_station = next_station  
       
    def choose_next_station(self) -> str:
        destination_list = list(self.current_station.connections.keys())   
        next_station = (destination_list[random.randint(0, len(destination_list) - 1)])                 
        return next_station
    
    def update_travel_time(self, next_station: Station) -> None:
        self.travel_time += self.current_station.connections[str(next_station.station_number)]
        
    def travel_time_zero(self) -> None:
        self.travel_time = 0
    
    def empty_destination_history(self) -> None:
        self.destination_history = [self.current_station.station_name]     
                