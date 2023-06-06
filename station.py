from typing import Dict


class Station:
    def __init__(self, station_name: str, y: float, x: float):
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