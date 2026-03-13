from fastapi import FastAPI
from pydantic import BaseModel

from ml.feature_builder import build_feature_vector
from ml.prediction import predict_delay
from routing.route_optimizer import find_best_route


app = FastAPI(
    title="Logistics Delay & Route Optimization API",
    description="Predict shipment delay and suggest optimal routes",
    version="1.0"
)

class ShipmentRequest(BaseModel):
    source: str
    destination: str
    time: str


# ===============================
# BASIC HEALTH CHECK
# ===============================

@app.get("/")
def home():

    return {
        "message": "Logistics Delay Prediction API running"
    }



@app.post("/predict-delay")
def predict_delay_api(request: ShipmentRequest):

    try:

        features = build_feature_vector(
            request.source,
            request.destination,
            request.time
        )

        prob, delay = predict_delay(features)

        return {
            "source": request.source,
            "destination": request.destination,
            "delay_probability": prob,
            "delay_prediction": delay
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/optimize-route")
def optimize_route(request: ShipmentRequest):

    result = find_best_route(
        request.source,
        request.destination,
        request.time
    )

    return result