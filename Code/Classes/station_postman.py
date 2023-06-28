#!/usr/bin/env python 
"""
Station class used in the Postman Tour.
Does not make use of station numbers.
"""
from typing import Dict, List, Type, Iterator, Any

class IterInstances(type):
    def __iter__(cls: Type['Station_Postman']) -> Iterator['Station_Postman']:
        return iter(cls._instances)

class Station_Postman(metaclass=IterInstances):
    """
    Class representing stations in the Postman Tour algorithm.

    Attributes:
    - - - - - - -  
    - station_name: str
        the name of the station 
    - connections: Dict[str, Dict[str, int]]
        the other stations that the station is connected to, 
        and how long the travel time is
    - visited: bool
        if the station has been visited by the train
    """
    _instances: List[Any] = []

    def __init__(self, station_name: str):
        self._instances.append(self)
        self.station_name = station_name
        self.connections: Dict[str, Dict[str, int]] = {}
        self.visited = False

    def add_connection(self, station_name: str, travel_time: int) -> None:
        """
        Adds connection to a station. 
        """
        self.connections[station_name] = travel_time