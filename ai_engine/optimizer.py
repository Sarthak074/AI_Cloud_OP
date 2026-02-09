def generate_recommendations(df):
    recs = []

    # ---- CPU Optimization ----
    avg_cpu = df["cpu_usage"].tail(10).mean()
    cpu_pred_next = df["cpu_pred"].iloc[-1]

    if avg_cpu > 80:
        recs.append("High CPU usage detected — consider scaling container resources.")

    if cpu_pred_next > 85:
        recs.append("AI predicts CPU usage will exceed 85% soon — proactive scaling recommended.")

    # ---- Memory Optimization ----
    avg_mem = df["memory_usage"].tail(10).mean()

    if avg_mem > 75:
        recs.append("High memory pressure — consider increasing memory limits.")

    # ---- Latency Optimization ----
    avg_lat = df["latency"].tail(10).mean()
    overall_lat_mean = df["latency"].mean()

    if avg_lat > overall_lat_mean * 1.5:
        recs.append("Latency anomaly detected — check API performance or network delays.")

    # ---- Anomaly Alerts ----
    recent_anom = df["anomaly"].tail(10)
    if (recent_anom == -1).sum() > 2:
        recs.append("Multiple anomalies detected — potential resource leak or abnormal behavior.")

    # ---- Failure Prediction (optional) ----
    if "fail_pred" in df.columns:
        if df["fail_pred"].iloc[-1] == 1:
            recs.append("High probability of failure — immediate action required.")

    # ---- No warnings ----
    if not recs:
        recs.append("System stable — no optimization actions required.")

    return recs
