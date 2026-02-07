from fastapi import FastAPI
import pandas as pd
from ai_engine.ai_engine import run_ai_pipeline   # we will create a simple function

app = FastAPI()

# Load latest metrics + AI results
def load_latest_df():
    cpu = pd.read_csv("./ai_engine/cpu_metrics.csv")
    mem = pd.read_csv("./ai_engine/memory_metrics.csv")
    lat = pd.read_csv("./ai_engine/latency_metrics.csv")

    df = cpu.merge(mem, on="timestamp", how="outer")
    df = df.merge(lat, on="timestamp", how="outer")
    df = df.sort_values("timestamp").ffill().fillna(0)

    return df


@app.get("/")
def root():
    return {"status": "Backend API running!"}


@app.get("/metrics")
def get_metrics():
    df = load_latest_df()
    return df.tail(10).to_dict(orient="records")


@app.get("/predict")
def get_predictions():
    df, _ = run_ai_pipeline()
    return {
        "latest_cpu": float(df["cpu_usage"].iloc[-1]),
        "predicted_cpu": float(df["cpu_pred"].iloc[-1]),
        "anomaly": int(df["anomaly"].iloc[-1]),
    }


@app.get("/anomalies")
def get_anomalies():
    df, _= run_ai_pipeline()
    anomalies = df[df["anomaly"] == -1]
    return anomalies.tail(10).to_dict(orient="records")


@app.get("/recommendations")
def get_recommendations():
    df, recs = run_ai_pipeline()
    return {"recommendations": recs}
