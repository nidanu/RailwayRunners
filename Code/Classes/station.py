#!/usr/bin/env python # 
"""
Configuration of a station class for all stations.
"""

from typing import Dict, List, Type, Iterator, Any

class IterInstances(type):
    def __iter__(self,cls: Type['Station']) -> Iterator['Station']:
        return iter(cls._instances)

class Station(metaclass=IterInstances):
    """
    Station class representing a station, its location in coordinates, 
    if it has been visited, and its connections

    Attributes:
    - - - - - - - 
    - station number: int
        the number of the station 
    - station_name: str
        the name of the station 
    - connections: Dict[str, int]
        the other stations that the station is connected to, 
        and how long the travel time is
    - visited: bool
        if the station has been visited by the train
    - y : int
        y-coordinate of its location
    - x : int
        x-coordinate of its location
    """
    _instances: List[Any] = []

    def __init__(self, station_number: int, station_name: str, y: float, x: float):
        self._instances.append(self)
        self.station_number = station_number
        self.station_name = station_name
        self.connections: Dict[str, int] = {}
        self.visited = False
        self.y = y
        self.x = x

    def add_connection(self, station: str, travel_time: int) -> None:
        """
        Adds connection to a station. 
        """
        self.connections[str(station)] = int(travel_time)

    def check_connection(self, station: str) -> bool:
        """
        Determines if a station is connected to a given station. Returns
        True if the connection exist, False otherwise.
        """
        if station in self.connections.keys():
            return True
        else:
            return False
        
        
