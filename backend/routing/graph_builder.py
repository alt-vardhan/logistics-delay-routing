import pandas as pd
import networkx as nx
from .route_generator import get_coordinates
from utils.distance import haversine
from ml.feature_builder import build_feature_vector
from ml.prediction import predict_delay, explain_prediction


network = pd.read_csv("data/network.csv")


def build_delay_graph(time):

    G = nx.Graph()

    for _, row in network.iterrows():

        src = row["source"]
        dst = row["destination"]

        lat1, lon1 = get_coordinates(src)
        lat2, lon2 = get_coordinates(dst)

        distance = haversine(lat1, lon1, lat2, lon2)

        # build features for ML prediction
        features = build_feature_vector(src, dst, time)

        prob, _ = predict_delay(features)

        top_factors = explain_prediction(features)

        # hybrid edge cost
        cost = distance + (100 * prob)

        G.add_edge(
            src,
            dst,
            weight=cost,
            distance=distance,
            delay_prob=prob,
            explanation=top_factors
        )

    return G