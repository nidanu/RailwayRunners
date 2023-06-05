class Connection:
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

    def check_connection(self, station):
        if self.station2 == station:
            return True
        else:
            return False