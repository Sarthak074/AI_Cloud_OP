def generate_recommendations(df):
    recs = []

    # ---- CPU Optimization ----
    avg_cpu = df["cpu_usage"].tail(10).mean()
    cpu_pred_next = df["cpu_pred"].iloc[-1]

    if avg_cpu > 80:
        recs.append("⚠ High CPU usage detected — consider scaling container resources or adding replicas.")

    if cpu_pred_next > 85:
        recs.append("🧠 AI predicts CPU usage will exceed 85% soon — proactive scaling recommended.")

    # ---- Memory Optimization ----
    avg_mem = df["memory_usage"].tail(10).mean()

    if avg_mem > 75:
        recs.append("⚠ High memory pressure — optimize application memory or increase memory limits.")

    # ---- Latency Optimization ----
    avg_lat = df["latency"].tail(10).mean()

    if avg_lat > df["latency"].mean() * 1.5:
        recs.append("⚠ Latency anomaly detected — inspect API performance or network issues.")

    # ---- Anomaly Alerts ----
    recent_anom = df["anomaly"].tail(10)
    if (recent_anom == -1).sum() > 2:
        recs.append("🚨 Multiple anomalies detected — potential resource leak or abnormal container behavior.")

    # ---- Failure Risk ----
    fail_pred = df["fail_pred"].iloc[-1]
    if fail_pred == 1:
        recs.append("🔥 High probability of failure predicted — immediate action recommended.")

    # If no recommendations
    if not recs:
        recs.append("✅ System stable — no optimization actions required.")

    return recs
