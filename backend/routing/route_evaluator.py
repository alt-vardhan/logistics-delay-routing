from .path_finder import find_best_path


def evaluate_delay_route(source, destination, time):

    path, G = find_best_path(source, destination, time)

    segments = []

    total_distance = 0
    total_delay = 0

    for i in range(len(path)-1):

        src = path[i]
        dst = path[i+1]

        edge = G[src][dst]

        total_distance += edge["distance"]
        total_delay += edge["delay_prob"]

        segments.append({
            "from": src,
            "to": dst,
            "distance": edge["distance"],
            "delay_probability": edge["delay_prob"],
            "top_delay_factors": edge["explanation"]
        })

    cost = total_distance + 100 * total_delay

    return {
        "route": path,
        "distance": total_distance,
        "delay_risk": total_delay,
        "cost": cost,
        "segments": segments
    }