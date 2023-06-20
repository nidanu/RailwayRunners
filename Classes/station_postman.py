#!/usr/bin/env python 
"""
Inherited class from Station object. Does not make use of station numbers.
"""

from .station import Station
from typing import Dict

class Station_Postman(Station):
    def __init__(self, station_name: str, y: float, x: float):
        self._instances.append(self)
        self.station_name = station_name
        self.connections: Dict[str, int] = {}
        self.visited = False
        self.y = y
        self.x = x
