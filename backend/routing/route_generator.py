import pandas as pd

hubs = pd.read_csv("data/hubs.csv")

def generate_routes(source, destination):

    routes = []

    # direct route
    routes.append([source, destination])

    # routes with hubs
    for hub in hubs["city"]:

        if hub != source and hub != destination:
            routes.append([source, hub, destination])

    return routes

def get_coordinates(city):

    row = hubs[hubs["city"] == city]

    if len(row) == 0:
        raise ValueError("City not found")

    lat = float(row.iloc[0]["lat"])
    lon = float(row.iloc[0]["lon"])

    return lat, lon