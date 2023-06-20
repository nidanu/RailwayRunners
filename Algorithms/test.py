from postman import *
from dijkstra import *

sys.path.append("..")
from Classes.station_postman import *
from Code.load_info import *
from Code.functions import *
from Visualisation.network import *
from Visualisation.scatter import *

if __name__ == '__main__':

    filename_connections = "../Cases/Holland/ConnectiesHolland.csv"
    filename_stations = "../Cases/Holland/StationsHolland.csv"

    hol_stations = "../Cases/Netherlands/StationsNationaal.csv"
    hol_connections = "../Cases/Netherlands/ConnectiesNationaal.csv"
    stations, Station, total_connections = load(filename_stations, filename_connections)
    results = "../Results/random_results.csv"
    vertices = []
    graph = {}

    for station in Station:
        graph[station.station_name] = station.connections
        vertices.append(station.station_name)

    """circuit, total_weight, trajectories = Postman.run_postman(vertices, graph)
    for trajector in trajectories:
        print(len(trajectories))
        print(trajector, '\n\n')
    score = Postman.calculate_score(circuit, total_weight, trajectories, total_connections)
    print(score)"""
    
    scores = []

    for i in range(1000):
        circuit, total_weight, trajectories = Postman.run_postman(vertices, graph)
        if len(trajectories) <= 7:
            scores.append(Postman.calculate_score(circuit, total_weight, trajectories, total_connections))
    print(max(scores))
    #waarin K de kwaliteit van de lijnvoering is, p de fractie van de bereden verbindingen (dus tussen 0 en 1), 
    #T het aantal trajecten en Min het aantal minuten in alle trajecten samen.
    """
        K = p*10000 - (T*100 + Min)
        if len(traj) <= 7:
            good.append((weight, traj))
    print(good)"""

    #network_map(Station)

   # scatter_plot(results)


