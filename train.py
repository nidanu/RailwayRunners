class Train:
    def __init__(self, start_station):
        self.train_name = start_station
        self.travel_time = 0
        self.destination_history = []     

    def add_destination(self, station, travel_time):
       self.destination_history.append(station)
       self.travel_time += travel_time

    def check_destination(self, station):
       if station in self.destination_history:
           return True
       else:
           return False