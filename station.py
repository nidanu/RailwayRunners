class Station:
    def __init__(self, station_name, y, x):
        self.station_name = station_name
        self.connections = {}
        self.visited = False
        self.y = y
        self.x = x


    def add_connection(self, station, time):
       self.connections[station] = time


    def check_connection(self, station):
       if station in self.connections.keys():
           return True
       else:
           return False