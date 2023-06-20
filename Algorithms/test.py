from postman import *
from dijkstra import *

sys.path.append("..")
from Classes.station import *
from Code.functions import *


if __name__ == '__main__':
    connections = "../Cases/Holland/ConnectiesHolland.csv"
    stations = "../Cases/Holland/StationsHolland.csv"
    stations_list = create_list_of_stations(stations)
    create_station_connections(stations, connections, stations_list)
    for station in stations_list:
        print(station.station_name, station.connections)

    vertices = []
    graph = {}
    for station in Station:
        graph[station.station_name] = station.connections
        vertices.append(station.station_name)
    circuit, weight = Postman.run_postman(vertices, graph)
    print(circuit, weight)
