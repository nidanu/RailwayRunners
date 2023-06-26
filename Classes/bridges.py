# A Python program to print Eulerian trail in a
# given Eulerian or Semi-Eulerian Graph(vikramshirsath177) https://www.geeksforgeeks.org/paths-travel-nodes-using-edgeseven-bridges-konigsberg/
import sys 
from collections import defaultdict
sys.path.append('..')
from Code.load_info import create_list_of_stations, create_station_connections 


class Graph:	
    # Constructor and destructor
    def __init__(self, V, station_number, stations, num_stations, max_time, list_connections, file_connections):
        self.V = V
        self.adj = defaultdict(list)

        self.all_stations_visited = False
        
        self.travel_time_train = 0
        self.train_count = 1
        self.total_time_network = 0        
        
        self.stations_visited = []       
        self.stations = stations
        self.starting_station = station_number
        self.num_stations = num_stations
        self.max_time = max_time
        self.list_connections = list_connections     
        self.file_connections = file_connections

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
        
    def printEulerUtil(self, u):		
        
        if self.stations[u].station_name not in self.stations_visited:
            self.stations_visited.append(self.stations[u].station_name)
            
        if len(self.stations_visited) == self.num_stations and self.all_stations_visited == False:	
            self.total_time_network += self.travel_time_train		
            print(f"ROUTE {self.train_count}: {self.travel_time_train} minutes")         
               
            p = 1 - (len(self.list_connections) / self.num_stations)       
            self.final_score = (10000 * p) - ((self.train_count*100) + self.total_time_network)    

            with open(self.file_connections, "r") as f:
                next(f)
                self.list_connections = []
                list_connection_lengths = []
                for connection in f.readlines():
                    cur_connection = connection.split(",")
                    clean_connection = cur_connection[0:2]
                    self.list_connections.append(clean_connection)            
                    list_connection_lengths.append(float(cur_connection[2]))              
                
            self.all_stations_visited = True
            self.stations_visited = []          
            
                    
        # Recur for all the vertices adjacent to this vertex
        if len(self.stations_visited) < self.num_stations and self.all_stations_visited == False:
            for v in self.adj[u]:                
                # If edge u-v is not removed and it's a valid next edge
                if v != -1 and self.isValidNextEdge(u, v):                                      
                    if self.travel_time_train + self.stations[int(u)].connections[str(v)] > self.max_time and self.all_stations_visited == False:
                        print(f"ROUTE {self.train_count}: {self.travel_time_train} minutes")
                        self.train_count += 1
                        self.total_time_network += self.travel_time_train 
                        self.travel_time_train = 0                                        
                        print()
                        
                    if self.all_stations_visited == False:
                        print(self.stations[u].station_name, "-", self.stations[v].station_name)          
                        
                        for i in range(len(self.list_connections)):                             

                            # Delete visited connection from list of connections
                            if self.list_connections[i][0] == self.stations[u].station_name and self.list_connections[i][1] ==  self.stations[v].station_name:
                                current_connection = i                    
                                self.list_connections.pop(current_connection)
                                break
                            elif self.list_connections[i][0] ==  self.stations[v].station_name and self.list_connections[i][1] == self.stations[u].station_name:
                                current_connection = i                   
                                self.list_connections.pop(current_connection)
                                break              
                
                    self.travel_time_train += self.stations[int(u)].connections[str(v)]                			
                                    
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
    