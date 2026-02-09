import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import joblib
import os

from ai_engine.optimizer import generate_recommendations


def run_ai_pipeline():
    model_dir = "ai_engine/models"
    os.makedirs(model_dir, exist_ok=True)

    print("\n=== LOADING METRICS ===")

    cpu_df = pd.read_csv("ai_engine/cpu_metrics.csv")
    mem_df = pd.read_csv("ai_engine/memory_metrics.csv")
    lat_df = pd.read_csv("ai_engine/latency_metrics.csv")

    df = cpu_df.merge(mem_df, on="timestamp", how="outer")
    df = df.merge(lat_df, on="timestamp", how="outer")
    df = df.sort_values("timestamp")
    df = df.ffill().fillna(0)

    # -----------------------------------------------------
    # FIX 1 — SCALE CPU USAGE (Docker returns tiny values)
    # -----------------------------------------------------
    df["cpu_usage"] = df["cpu_usage"] * 100

    # -----------------------------------------------------
    # FIX 2 — BUILD LAG FEATURES
    # -----------------------------------------------------
    print("\n=== BUILDING AUTOREGRESSIVE FEATURES ===")

    for i in range(1, 6):
        df[f"cpu_lag_{i}"] = df["cpu_usage"].shift(i)

    df = df.fillna(0)

    # -----------------------------------------------------
    # MODEL 1 — CPU SPIKE PREDICTION
    # -----------------------------------------------------
    print("\n=== TRAINING CPU PREDICTOR (Lag Model) ===")

    # Drop early rows with missing lags
    df = df.dropna(subset=["cpu_lag_1", "cpu_lag_2", "cpu_lag_3", "cpu_lag_4", "cpu_lag_5"])

    X_cpu = df[["cpu_lag_1", "cpu_lag_2", "cpu_lag_3", "cpu_lag_4", "cpu_lag_5"]]
    y_cpu = df["cpu_usage"]

    lr = LinearRegression()
    lr.fit(X_cpu, y_cpu)

    df["cpu_pred"] = lr.predict(X_cpu)

    joblib.dump(lr, f"{model_dir}/cpu_model.pkl")

    # save plot
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["cpu_usage"], label="CPU Actual")
    plt.plot(df["timestamp"], df["cpu_pred"], label="CPU Predicted")
    plt.legend()
    plt.title("CPU Prediction (Autoregressive)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("ai_engine/plots/cpu_prediction.png")
    plt.close()

    # -----------------------------------------------------
    # MODEL 2 — ANOMALY DETECTION
    # -----------------------------------------------------
    print("\n=== TRAINING ANOMALY DETECTOR ===")

    X_anom = df[["cpu_usage", "memory_usage", "latency"]]

    iso = IsolationForest(contamination=0.05)
    df["anomaly"] = iso.fit_predict(X_anom)

    joblib.dump(iso, f"{model_dir}/anomaly_model.pkl")

    # anomaly plot
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["cpu_usage"], label="CPU")
    plt.scatter(
        df["timestamp"][df["anomaly"] == -1],
        df["cpu_usage"][df["anomaly"] == -1],
        color="red",
        label="Anomaly"
    )
    plt.legend()
    plt.title("CPU Anomaly Detection")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("ai_engine/plots/anomaly_plot.png")
    plt.close()

    # -----------------------------------------------------
    # MODEL 3 — FAILURE PREDICTION
    # -----------------------------------------------------
    print("\n=== TRAINING FAILURE PREDICTOR ===")

    df["failure"] = (df["cpu_usage"] > df["cpu_usage"].mean() * 2).astype(int)

    X_fail = df[["cpu_lag_1", "cpu_lag_2", "cpu_lag_3"]]
    y_fail = df["failure"]

    if y_fail.nunique() < 2:
        print("⚠️ Not enough failure events. Skipping model.")
        joblib.dump(None, f"{model_dir}/failure_model.pkl")
        df["fail_pred"] = 0
    else:
        logr = LogisticRegression()
        logr.fit(X_fail, y_fail)
        df["fail_pred"] = logr.predict(X_fail)
        joblib.dump(logr, f"{model_dir}/failure_model.pkl")

    # -----------------------------------------------------
    # OPTIMIZATION RECOMMENDATIONS
    # -----------------------------------------------------
    print("\n=== GENERATING OPTIMIZATION RECOMMENDATIONS ===")
    recommendations = generate_recommendations(df)

    return df, recommendations


if __name__ == "__main__":
    run_ai_pipeline()