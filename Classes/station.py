#!/usr/bin/env python # 
"""
Configuration of a station class for all stations.
"""

from typing import Dict, List, Type, Iterator

class IterInstances(type):
    def __iter__(cls: Type['Station']) -> Iterator['Station']:
        return iter(cls._instances)

class Station(metaclass=IterInstances):
    _instances = []

    def __init__(self, station_number: int, station_name: str, y: float, x: float):
        self._instances.append(self)
        self.station_number = station_number
        self.station_name = station_name
        self.connections: Dict[str, int] = {}
        self.visited = False
        self.y = y
        self.x = x

    def add_connection(self, station: str, travel_time: int) -> None:
        self.connections[station] = travel_time

    def check_connection(self, station: str) -> bool:
        if station in self.connections.keys():
            return True
        else:
            return False
        
        
