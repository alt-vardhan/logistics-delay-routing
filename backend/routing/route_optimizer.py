from .route_evaluator import evaluate_delay_route


def find_best_route(source, destination, time):

    result = evaluate_delay_route(source, destination, time)

    return result