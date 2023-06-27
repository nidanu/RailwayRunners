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
    _instances: List[Any] = []

    def __init__(self, station_name: str):
        self._instances.append(self)
        self.station_name = station_name
        self.connections: Dict[str, int] = {}
        self.visited = False

    def add_connection(self, station_name: str, travel_time: int) -> None:
        self.connections[station_name] = travel_time

    def get_connection(self):
        return list(self.connections.keys())
