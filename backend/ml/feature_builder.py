import pandas as pd
import requests
import random
from datetime import datetime


# ===============================
# MODEL FEATURE ORDER
# ===============================

MODEL_FEATURES = [
    "Latitude",
    "Longitude",
    "Temperature",
    "Humidity",
    "Waiting_Time",
    "Demand_Forecast",
    "hour",
    "day",
    "dayofweek",
    "is_weekend",
    "Traffic_Status_Detour",
    "Traffic_Status_Heavy",
    "congestion_index",
    "is_peak_hour",
    "peak_traffic_risk",
    "weather_stress",
    "relative_demand_pressure",
    "delay_pressure"
]


# ===============================
# TIME FEATURES
# ===============================

def extract_time_features(time_str):

    dt = datetime.fromisoformat(time_str)

    return {
        "hour": dt.hour,
        "day": dt.day,
        "dayofweek": dt.weekday(),
        "is_weekend": int(dt.weekday() >= 5)
    }


# ===============================
# GET COORDINATES
# ===============================

def get_coordinates(city):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

    headers = {"User-Agent": "delay-predictor"}

    r = requests.get(url, headers=headers).json()

    lat = float(r[0]["lat"])
    lon = float(r[0]["lon"])

    return lat, lon


# ===============================
# WEATHER DATA
# ===============================

def get_weather(city):

    API_KEY = "4ae94042b1c1b6e54fdec73f9c9022e9"

    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        r = requests.get(url).json()

        return {
            "Temperature": r["main"]["temp"],
            "Humidity": r["main"]["humidity"]
        }

    except:

        return {
            "Temperature": 30,
            "Humidity": 50
        }


# ===============================
# TRAFFIC ESTIMATION
# ===============================

def estimate_traffic(hour):

    if 8 <= hour <= 10 or 17 <= hour <= 19:
        return "Heavy"

    elif 11 <= hour <= 16:
        return "Detour"

    else:
        return "Clear"


def encode_traffic(status):

    return {
        "Traffic_Status_Heavy": int(status == "Heavy"),
        "Traffic_Status_Detour": int(status == "Detour")
    }


# ===============================
# DEMAND FORECAST
# ===============================

def get_demand(hour):

    demand_by_hour = {
        8: 230,
        9: 250,
        10: 210,
        11: 200,
        12: 190,
        13: 210,
        14: 220,
        15: 230,
        16: 240,
        17: 260,
        18: 270
    }

    return demand_by_hour.get(hour, 200)


# ===============================
# WAITING TIME
# ===============================

def estimate_waiting_time(traffic):

    if traffic == "Heavy":
        return random.uniform(20, 40)

    if traffic == "Detour":
        return random.uniform(10, 20)

    return random.uniform(3, 10)


# ===============================
# FEATURE ENGINEERING
# ===============================

def build_engineered_features(features):

    features["congestion_index"] = (
        features["Traffic_Status_Heavy"] +
        0.7 * features["Traffic_Status_Detour"]
    )

    features["is_peak_hour"] = int(
        features["hour"] in [8, 9, 10, 17, 18, 19]
    )

    features["peak_traffic_risk"] = (
        features["is_peak_hour"] *
        (features["Traffic_Status_Heavy"] + features["Traffic_Status_Detour"])
    )

    features["weather_stress"] = (
        abs(features["Temperature"] - 25) +
        abs(features["Humidity"] - 50)
    )

    features["relative_demand_pressure"] = (
        features["Demand_Forecast"] / 200
    )

    features["delay_pressure"] = (
        features["Waiting_Time"] *
        (1 + features["Traffic_Status_Heavy"] + features["Traffic_Status_Detour"])
    )

    return features


# ===============================
# BUILD FEATURE VECTOR
# ===============================

def build_feature_vector(source, destination, time_str):

    time_features = extract_time_features(time_str)

    lat, lon = get_coordinates(source)

    weather = get_weather(source)

    traffic = estimate_traffic(time_features["hour"])

    traffic_encoded = encode_traffic(traffic)

    demand = get_demand(time_features["hour"])

    waiting = estimate_waiting_time(traffic)

    features = {
        "Latitude": lat,
        "Longitude": lon,
        "Temperature": weather["Temperature"],
        "Humidity": weather["Humidity"],
        "Waiting_Time": waiting,
        "Demand_Forecast": demand,
        **time_features,
        **traffic_encoded
    }

    features = build_engineered_features(features)

    df = pd.DataFrame([features])

    df = df[MODEL_FEATURES]

    return df