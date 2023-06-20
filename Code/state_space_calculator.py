"""
name: state_space_calculator.py

Description:
Calculates amount of options based on the avarige amount of connections per station and the avarage amount of stations visited

    Naming:
    c = connections
    r = route
    s = station
    
    Results
    Holland =     13226439
    Netherlands = 724161050256872386310617526939156480
    Costum =      To be calculated 
"""

# Instructuins and input request
print("h = Holland")
print("n = Netherlands")
print("c = custom")
size = input("What size? ")

# Checks input until valid
while size not in ["h", "n", "c"]:
    print("invalid input, please try again.")
    size = input("What size? ")

# Picks right variables 
if size == "h":
    min_time = 381
    n_connections = 28
    n_stations = 22
    r_length = 120
    max_routes = 7
elif size == "n":
    min_time = 1551
    n_connections = 89
    n_stations = 60
    r_length = 180
    max_routes = 20
elif size == "c":
    min_time = int(input("What is the sum of the travel duration of all connections? "))
    n_connections = int(input("How many connections? "))
    n_stations = int(input("How many stations?"))
    r_length = int(input("What is the maximum length of a route?"))
    max_routes = int(input("What is the maximum ammount of routes?"))    

# Setting empty variables 
avg_n_s = 0.0
state_space = 0.0

# State space calculation
time = r_length * max_routes
avg_c_s = n_connections / n_stations
avg_c = (min_time / n_connections)
while time >= min_time:
    if (time % r_length) < avg_c:
        time -= time % r_length
    avg_n_s = time / avg_c
    state_space += avg_c_s ** avg_n_s
    time -= avg_c

# Displays outcome 
print(state_space)

