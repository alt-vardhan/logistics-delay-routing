import joblib
import shap
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "model" / "delay_model.pkl"

model = joblib.load(MODEL_PATH)

explainer = shap.TreeExplainer(model)
# ===============================
# PREDICT DELAY
# ===============================

def predict_delay(features):

    prob = model.predict_proba(features)[0][1]

    delay = prob >= 0.40

    return float(prob), bool(delay)


# ===============================
# SHAP EXPLANATION
# ===============================

def explain_prediction(features, top_n=3):

    shap_values = explainer.shap_values(features)

    values = shap_values[0]

    feature_names = features.columns

    importance = []

    for name, val in zip(feature_names, values):

        importance.append((name, abs(val)))

    importance.sort(key=lambda x: x[1], reverse=True)

    top_features = [f[0] for f in importance[:top_n]]

    return top_features