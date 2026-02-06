import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

from optimizer import generate_recommendations

def run_ai_pipeline():
    print("\n=== LOADING METRICS ===")

    cpu_df = pd.read_csv("cpu_metrics.csv")
    mem_df = pd.read_csv("memory_metrics.csv")
    lat_df = pd.read_csv("latency_metrics.csv")

    # Merge all 3 datasets on timestamp
    df = cpu_df.merge(mem_df, on="timestamp", how="outer")
    df = df.merge(lat_df, on="timestamp", how="outer")

    df = df.sort_values("timestamp")
    df = df.ffill().fillna(0)   # Handle missing rows

    print(df.head())


    # --------------------------
    # FEATURE ENGINEERING 
    # --------------------------

    df["cpu_avg"]     = df["cpu_usage"].rolling(5).mean()
    df["cpu_trend"]   = df["cpu_usage"].diff()

    df["mem_avg"]     = df["memory_usage"].rolling(5).mean()
    df["mem_trend"]   = df["memory_usage"].diff()

    df["lat_avg"]     = df["latency"].rolling(5).mean()
    df["lat_trend"]   = df["latency"].diff()

    df = df.fillna(0)

    # Create failure label (just synthetic)
    df["failure"] = (df["cpu_usage"] > df["cpu_usage"].mean() * 2).astype(int)

    print("\n=== FINAL FEATURES ===")
    print(df.head())


    # -----------------------------------------
    # MODEL 1 — CPU PREDICTION (Linear Regression)
    # -----------------------------------------

    print("\n=== TRAINING CPU PREDICTOR ===")

    X_cpu = df[["cpu_trend", "mem_avg", "lat_avg"]]
    y_cpu = df["cpu_usage"]

    lr = LinearRegression()
    lr.fit(X_cpu, y_cpu)

    df["cpu_pred"] = lr.predict(X_cpu)

    rmse = np.sqrt(mean_squared_error(df["cpu_usage"], df["cpu_pred"]))
    print("CPU Prediction RMSE:", rmse)

    plt.figure(figsize=(10,4))
    plt.plot(df["timestamp"], df["cpu_usage"], label="CPU Actual")
    plt.plot(df["timestamp"], df["cpu_pred"], label="CPU Predicted")
    plt.legend()
    plt.title("CPU Prediction")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    # -----------------------------------------
    # MODEL 2 — ANOMALY DETECTION (Isolation Forest)
    # -----------------------------------------

    print("\n=== TRAINING ANOMALY DETECTOR ===")

    X_anom = df[["cpu_usage", "memory_usage", "latency"]]
    iso = IsolationForest(contamination=0.05)
    df["anomaly"] = iso.fit_predict(X_anom)

    plt.figure(figsize=(10,4))
    plt.plot(df["timestamp"], df["cpu_usage"], label="CPU")
    plt.scatter(df["timestamp"][df["anomaly"]==-1],
                df["cpu_usage"][df["anomaly"]==-1],
                label="Anomaly", marker="o", color="red")
    plt.legend()
    plt.title("CPU Anomaly Detection")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    # -----------------------------------------
    # MODEL 3 — FAILURE PREDICTION (Logistic Regression)
    # -----------------------------------------

    print("\n=== TRAINING FAILURE PREDICTOR ===")

    X_fail = df[["cpu_avg", "mem_avg", "lat_avg"]]
    y_fail = df["failure"]

    logr = LogisticRegression()
    logr.fit(X_fail, y_fail)

    df["fail_pred"] = logr.predict(X_fail)

    acc = accuracy_score(y_fail, df["fail_pred"])
    cm = confusion_matrix(y_fail, df["fail_pred"])

    print("Failure Prediction Accuracy:", acc)
    print("Confusion Matrix:\n", cm)

    plt.figure(figsize=(10,4))
    plt.scatter(df["timestamp"], df["fail_pred"], label="Pred")
    plt.scatter(df["timestamp"], df["failure"], label="Actual")
    plt.legend()
    plt.title("Failure Prediction")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\n=== GENERATING OPTIMIZATION RECOMMENDATIONS ===")
    recommendations = generate_recommendations(df)

    for r in recommendations:
        print(" -", r)
    
    return df, recommendations

if __name__=='main':
    run_ai_pipeline()
