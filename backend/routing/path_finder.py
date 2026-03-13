import networkx as nx
from .graph_builder import build_delay_graph


def find_best_path(source, destination, time):

    G = build_delay_graph(time)

    path = nx.shortest_path(
        G,
        source,
        destination,
        weight="weight"
    )

    return path, G