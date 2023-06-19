# A Python program to print Eulerian trail in a
# given Eulerian or Semi-Eulerian Graph(vikramshirsath177)
from collections import defaultdict

from Classes.station import create_list_of_stations, create_station_connections, Station


# Create list with all stations + connections
stations = create_list_of_stations("./Cases/Holland/StationsHolland.csv")
create_station_connections("./Cases/Holland/StationsHolland.csv", "./Cases/Holland/ConnectiesHolland.csv", stations)

# Count number of stations
with open("./Cases/Holland/StationsHolland.csv", "r") as f:
    next(f)
    num_stations = len(f.readlines())  

# Count number of connections
    with open( "./Cases/Holland/ConnectiesHolland.csv", "r") as f:
        next(f)       
        num_connections = len(f.readlines())     

stations_visited = []   


class Graph:	
    # Constructor and destructor
    def __init__(self, V, station_number):
        self.V = V
        self.adj = defaultdict(list)

        self.done = False
        self.head_count = 0
        self.travel_time = 0
        self.train_count = 1
        self.total_time = 0
        self.starting_station = station_number
        self.stations_visited = []

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
            u = self.starting_station
            for i in range(self.V):
                if len(self.adj[i]) % 2 == 1:
                    u = i
                    break
		
            # Print tour starting from oddv
            self.printEulerUtil(u)
            print()
		
    def printEulerUtil(self, u):		
		
        if stations[u].station_name not in self.stations_visited:
            self.stations_visited.append(stations[u].station_name)
            
        if len(self.stations_visited) == num_stations and self.done == False:	
            self.total_time += self.travel_time		
            print(f"{self.train_count}: {self.travel_time}")
            print(f"Starting station: {self.starting_station}")
            
            
            print(f"Total time: {self.total_time}")

            self.final_score = 10000 - ((self.train_count*100) + self.total_time)
            print(f"Score: {self.final_score}")
            self.done = True
            self.stations_visited = []
            
		
        # Recur for all the vertices adjacent to this vertex
        if len(stations_visited) < num_stations and self.done ==False:
            for v in self.adj[u]:
                # If edge u-v is not removed and it's a valid next edge
                if v != -1 and self.isValidNextEdge(u, v):                    
                    if self.travel_time + stations[u].connections[v] > 120 and self.done == False:
                        print(f"{self.train_count}: {self.travel_time}")
                        self.train_count += 1
                        self.total_time += self.travel_time 
                        self.travel_time = 0
					 
                        print()
                        
                    if self.done == False:
                        print(stations[u].station_name, "-", stations[v].station_name)
                    
                
                    self.travel_time += stations[u].connections[v]                			
				
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
    
    
    
    top_score = 0
    
    for l in range(num_stations):  
        g = "g" + str(l)
        
        g = Graph(num_stations, l)
        #print(g.done)
        
    
        with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
            next(f)       
            for i in range(num_connections):
                connection_str = f.readline()
                connection = connection_str.split(",")
        
                station_1 = connection[0]
                station_2 = connection[1]            
            
                for j in range(num_stations):
                    if stations[j].station_name == station_1:
                        save_station_1 = j                    
                    if stations[j].station_name == station_2:
                        save_station_2 = j
                    
                g.addEdge(save_station_1, save_station_2)
                g.addEdge(save_station_2, save_station_1)
            
        g.printEulerTour()	
        if g.final_score > top_score:
                top_score = g.final_score
        
    # Create and test RAILNL graph
    g = Graph(num_stations, 11)
    print(f"Top score: {top_score}")  
    print()    
    print("Best")

    with open("./Cases/Holland/ConnectiesHolland.csv", "r") as f:
        next(f)       
        for i in range(num_connections):
            connection_str = f.readline()
            connection = connection_str.split(",")
        
            station_1 = connection[0]
            station_2 = connection[1]            
            
            for j in range(num_stations):
                if stations[j].station_name == station_1:
                    save_station_1 = j                    
                if stations[j].station_name == station_2:
                    save_station_2 = j
                    
            g.addEdge(save_station_1, save_station_2)
            g.addEdge(save_station_2, save_station_1)
            
    g.printEulerTour()	
        
                  
if __name__ == "__main__":
    main()
	