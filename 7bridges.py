# A Python program to print Eulerian trail in a
# given Eulerian or Semi-Eulerian Graph(vikramshirsath177)
from collections import defaultdict

from Classes.station import Station
from Classes.train import Train

# Create list with all stations
stations = []
stations_visited = []

# Count number of stations
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())
    
# Count number of connections
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)       
    num_connections = len(f.readlines())  

# Create list of Station objects
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)

    for i in range(num_stations):
        station_info = f.readline().split(',')
        station_info = station_info
        station_name = station_info[0]
        
        station_y = float(station_info[1])
        station_x_str = station_info[2].split('\n')
        station_x = float(station_x_str[0]) 
        
        new_station = Station(station_name, station_y, station_x)
        stations.append(new_station)       
   
# Load connections into Station objects
with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
    next(f)
    for i in range(num_connections):    
        connection_str = f.readline()
        connection = connection_str.split(",")
        
        station_1 = connection[0]
        station_2 = connection[1]
        traveltime_str = connection[2].split('\n')        
        traveltime = int(float(traveltime_str[0]))

        for i in range(num_stations):
            if stations[i].station_name == station_1:
                stations[i].add_connection(station_2, traveltime)
            if stations[i].station_name == station_2:
                stations[i].add_connection(station_1, traveltime)  


class Graph:	
    # Constructor and destructor
    def __init__(self, V):
        self.V = V
        self.adj = defaultdict(list)
        
        self.head_count = 0
        self.travel_time = 0
        self.train_count = 1
        self.total_time = 0

    # Functions to add and remove edge
    def addEdge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def rmvEdge(self, u, v):
        self.adj[u].remove(v)
        self.adj[v].remove(u)

    # Methods to print Eulerian tour
    def printEulerTour(self):
        # Find a vertex with odd degree
        u = 0
        for i in range(self.V):
            if len(self.adj[i]) % 2 == 1:
                u = i
                break
		
        # Print tour starting from oddv
        self.printEulerUtil(u)
        print()
		
    def printEulerUtil(self, u):		
		
        if stations[u].station_name not in stations_visited:
            stations_visited.append(stations[u].station_name)

        if len(stations_visited) == num_stations:	
            self.total_time += self.travel_time		
            print(f"{self.train_count}: {self.travel_time}")
            print()
            print(10000 - ((5*100) + self.total_time))
            print(self.total_time)
            exit()
		
        # Recur for all the vertices adjacent to this vertex
		
        for v in self.adj[u]:
            # If edge u-v is not removed and it's a valid next edge
            if v != -1 and self.isValidNextEdge(u, v):
                if self.travel_time + stations[u].connections[stations[v].station_name] > 120:
                    print(f"{self.train_count}: {self.travel_time}")
                    self.train_count += 1
                    self.total_time += self.travel_time 
                    self.travel_time = 0
					
                    print()
				
                print(stations[u].station_name, "-", stations[v].station_name, " ", end="")
                print()
                
                self.travel_time += stations[u].connections[stations[v].station_name]                			
				
                self.head_count += 1
                self.rmvEdge(u, v)
                self.printEulerUtil(v)

    # The function to check if edge u-v can be considered
    # as next edge in Euler Tout
    def isValidNextEdge(self, u, v):
        # The edge u-v is valid in one of the following
        # two cases:

        # 1) If v is the only adjacent vertex of u
        count = 0  # To store count of adjacent vertices
        for i in self.adj[u]:
            if i != -1:
                count += 1
        if count == 1:
            return True

        # 2) If there are multiple adjacents, then u-v is not a bridge
        # Do following steps to check if u-v is a bridge
        # 2.a) count of vertices reachable from u
        visited = [False] * (self.V)
        count1 = self.DFSCount(u, visited)

        # 2.b) Remove edge (u, v) and after removing
        # the edge, count vertices reachable from u
        self.rmvEdge(u, v)
        visited = [False] * (self.V)
        count2 = self.DFSCount(u, visited)

        # 2.c) Add the edge back to the graph
        self.addEdge(u, v)

        # 2.d) If count1 is greater, then edge (u, v) is a bridge
        return False if count1 > count2 else True

    # A DFS based function to count reachable vertices from v

    def DFSCount(self, v, visited):
        # Mark the current node as visited
		
        visited[v] = True
        count = 1
        # Recur for all the vertices adjacent to this vertex
        for i in self.adj[v]:
            if not visited[i]:
                count += self.DFSCount(i, visited)
        return count
    # utility function to form edge between two vertices
    # source and dest

    def makeEdge(src, dest):
        graph.addEdge(src, dest)

# Driver program to test above functions


def main():
    # Create and test RAILNL graph
    g1 = Graph(num_stations)
	
    # Alkmaar - Hoorn
    g1.addEdge(0, 15)
    g1.addEdge(15, 0)

    # Alkmaar - Den Helder
    g1.addEdge(0, 10)
    g1.addEdge(10, 0)

    # Amsterdam Amstel - Amsterdam Zuid
    g1.addEdge(2, 5)
    g1.addEdge(5, 2)

    # Amsterdam Amstel - Amsterdam Centraal
    g1.addEdge(2, 3)
    g1.addEdge(3, 2)

    # Amsterdam Centraal - Amsterdam Sloterdijk
    g1.addEdge(3, 4)
    g1.addEdge(4, 3)

    # Amsterdam Sloterdijk - Haarlem
    g1.addEdge(4, 13)
    g1.addEdge(13, 4)

    # Amsterdam Sloterdijk - Zaandam
    g1.addEdge(4, 21)
    g1.addEdge(21, 4)

    # Amsterdam Zuid - Amsterdam Sloterdijk
    g1.addEdge(5, 4)
    g1.addEdge(4, 5)

    # Amsterdam Zuid - Schiphol Airport
    g1.addEdge(5, 20)
    g1.addEdge(20, 5)

    # Beverwijk - Castricum
    g1.addEdge(6, 7)
    g1.addEdge(7, 6)

    # Castricum - Alkmaar
    g1.addEdge(7, 0)
    g1.addEdge(0, 7)

    # Delft - Den Haag Centraal
    g1.addEdge(8, 9)
    g1.addEdge(9, 8)

    # Den Haag Centraal - Gouda
    g1.addEdge(9, 12)
    g1.addEdge(12, 9)

    # Den Haag Centraal - Leiden Centraal
    g1.addEdge(9, 16)
    g1.addEdge(16, 9)

    # Dordrecht - Rotterdam Centraal
    g1.addEdge(11, 18)
    g1.addEdge(18, 11)

    # Gouda - Alphen a/d Rijn
    g1.addEdge(12, 1)
    g1.addEdge(1, 12)

    # Haarlem - Beverwijk
    g1.addEdge(13, 6)
    g1.addEdge(6, 13)

    # Heemstede-Aerdenhout - Haarlem 
    g1.addEdge(14, 13)
    g1.addEdge(13, 14)

    # Leiden Centraal - Heemstede-Aerdenhout
    g1.addEdge(16, 14)
    g1.addEdge(14, 16)

    # Leiden Centraal - Alphen a/d Rijn
    g1.addEdge(16, 1)
    g1.addEdge(1, 16)

    # Leiden Centraal - Schiphol Airport
    g1.addEdge(16, 20)
    g1.addEdge(20, 16)

    # Rotterdam Alexander - Gouda
    g1.addEdge(17, 12)
    g1.addEdge(12, 17)

    # Rotterdam Centraal - Schiedam Centrum
    g1.addEdge(18, 19)
    g1.addEdge(19, 18)

    # Rotterdam Centraal - Rotterdam Alexander
    g1.addEdge(18, 17)
    g1.addEdge(17, 18)

    # Schiedam Centrum - Delft
    g1.addEdge(19, 8)
    g1.addEdge(8, 19)

    # Zaandam - Castricum
    g1.addEdge(21, 7)
    g1.addEdge(7, 21)

    # Zaandam - Beverwijk
    g1.addEdge(21, 6)
    g1.addEdge(6, 21)

    # Zaandam - Hoorn
    g1.addEdge(21, 15)
    g1.addEdge(15, 21)
	
    g1.printEulerTour()	
    
    
if __name__ == "__main__":
    main()
	