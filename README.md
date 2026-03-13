# AI Logistics Delay Prediction & Route Optimization

This project predicts shipment delays and suggests optimal routes using machine learning and graph routing.

## Features

- XGBoost delay prediction model
- Graph-based route optimization
- Hybrid cost routing (distance + delay risk)
- SHAP explainability
- FastAPI backend

## Tech Stack

- Python
- XGBoost
- NetworkX
- SHAP
- FastAPI

## API Endpoints

### Predict Delay
POST /predict-delay

### Optimize Route
POST /optimize-route

## Run the Project

pip install -r requirements.txt
uvicorn api:app --reload