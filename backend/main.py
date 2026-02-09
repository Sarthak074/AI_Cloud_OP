from fastapi import FastAPI, Request
import pandas as pd
import joblib
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ai_engine.ai_engine import run_ai_pipeline
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

MODEL_DIR = "ai_engine/models"

# -------------------------
# On startup – train model
# -------------------------
@app.on_event("startup")
def startup_event():
    print("Running AI training pipeline...")
    run_ai_pipeline()
    print("AI models trained.")
    load_models()


# -------------------------
# Load trained models
# -------------------------
models = {}

def load_models():
    global models
    cpu_path = f"{MODEL_DIR}/cpu_model.pkl"
    anom_path = f"{MODEL_DIR}/anomaly_model.pkl"
    fail_path = f"{MODEL_DIR}/failure_model.pkl"

    if os.path.exists(cpu_path):
        models["cpu"] = joblib.load(cpu_path)

    if os.path.exists(anom_path):
        models["anomaly"] = joblib.load(anom_path)

    if os.path.exists(fail_path):
        try:
            models["failure"] = joblib.load(fail_path)
        except:
            models["failure"] = None

    print("Loaded models:", list(models.keys()))


# -------------------------
# Build SAME lag features as training
# -------------------------
def add_lag_features(df):
    for i in range(1, 6):
        df[f"cpu_lag_{i}"] = df["cpu_usage"].shift(i)

    df = df.bfill()
    return df


# -------------------------
# Prepare dataset (CPU, MEM, LAT CSVs)
# -------------------------
def load_feature_df():
    cpu = pd.read_csv("ai_engine/cpu_metrics.csv")
    mem = pd.read_csv("ai_engine/memory_metrics.csv")
    lat = pd.read_csv("ai_engine/latency_metrics.csv")

    df = cpu.merge(mem, on="timestamp", how="outer")
    df = df.merge(lat, on="timestamp", how="outer")
    df = df.sort_values("timestamp").ffill().fillna(0)

    df["cpu_usage"] = df["cpu_usage"] * 100

    # ADD LAG FEATURES (same as training)
    df = add_lag_features(df)

    # Predict CPU
    if "cpu" in models:
        try:
            df["cpu_pred"] = models["cpu"].predict(
                df[[f"cpu_lag_{i}" for i in range(1,6)]]
            )
        except Exception as e:
            print("CPU Prediction Error:", e)
            df["cpu_pred"] = 0
    else:
        df["cpu_pred"] = 0

    # Predict anomalies
    if "anomaly" in models:
        try:
            df["anomaly"] = models["anomaly"].predict(
                df[["cpu_usage", "memory_usage", "latency"]]
            )
        except:
            df["anomaly"] = 1
    else:
        df["anomaly"] = 1

    return df


# -------------------------
# ROUTES
# -------------------------
@app.get("/")
def root():
    return {"status": "AI Backend Online"}


@app.get("/metrics")
def get_metrics():
    df = load_feature_df()
    df["cpu_pred"] = df["cpu_pred"].astype(float)
    return df.tail(10).to_dict(orient="records")


@app.get("/predict")
def get_predictions():
    df = load_feature_df()
    last = df.iloc[-1]

    # CPU Prediction Feature Vector
    cpu_X = [[last[f"cpu_lag_{i}"] for i in range(1, 6)]]
    cpu_pred = models["cpu"].predict(cpu_X)[0]

    # Anomaly Detection
    anom_X = [[last["cpu_usage"], last["memory_usage"], last["latency"]]]
    anomaly = models["anomaly"].predict(anom_X)[0]

    return {
        "latest_cpu": float(last["cpu_usage"]),
        "predicted_cpu": float(cpu_pred),
        "anomaly": int(anomaly)
    }


@app.get("/anomalies")
def get_anomalies():
    df = load_feature_df()
    return df[df["anomaly"] == -1].tail(10).to_dict(orient="records")


@app.get("/recommendations")
def get_recommendations():
    from ai_engine.optimizer import generate_recommendations
    df = load_feature_df()
    recs = generate_recommendations(df)
    return {"recommendations": recs}


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
