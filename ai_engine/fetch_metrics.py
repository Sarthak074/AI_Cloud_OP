import requests
import pandas as pd
import time
from datetime import datetime

PROMETHEUS = "http://localhost:9090/api/v1/query_range"

def fetch_cpu_usage(container="load-generator"):
    end = int(time.time())            # current UNIX seconds
    start = end - 600                 # last 10 minutes

    query = f'rate(container_cpu_usage_seconds_total{{name="{container}"}}[30s])'

    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": "30s"
    }

    print("Sending CPU params:", params)

    response = requests.get(PROMETHEUS, params=params)
    print("Raw CPU response:", response.text)

    data = response.json()

    if data["status"] != "success":
        print("Query failed:", data)
        return None

    results = data["data"]["result"]
    if not results:
        print("No CPU metrics returned. Check the container name.")
        return None

    timestamps = []
    values = []

    for t, v in results[0]["values"]:
        timestamps.append(datetime.fromtimestamp(float(t)))
        values.append(float(v))

    df = pd.DataFrame({"timestamp": timestamps, "cpu_usage": values})
    df.to_csv("cpu_metrics.csv", index=False)

    print("Saved as cpu_metrics.csv")
    return df

def fetch_memory_usage(container="load-generator"):
    end = int(time.time())            # current UNIX seconds
    start = end - 600                 # last 10 minutes

    query = f'container_memory_usage_bytes{{name="{container}"}}'

    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": "30s"
    }

    print("Sending MEM params:", params)

    response = requests.get(PROMETHEUS, params=params)
    print("Raw MEM response:", response.text)

    data = response.json()

    if data["status"] != "success":
        print("Query failed:", data)
        return None

    results = data["data"]["result"]
    if not results:
        print("No memory metrics returned. Check the container name.")
        return None

    timestamps = []
    values = []

    for t, v in results[0]["values"]:
        timestamps.append(datetime.fromtimestamp(float(t)))
        values.append(float(v))

    df = pd.DataFrame({"timestamp": timestamps, "memory_usage": values})
    df.to_csv("memory_metrics.csv", index=False)

    print("Saved as memory_metrics.csv")
    return df

if __name__ == "__main__":
    fetch_cpu_usage()
    fetch_memory_usage()