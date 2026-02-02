import requests
import pandas as pd
from datetime import datetime, timedelta

PROMETHEUS="http://localhost:9090/api/v1/query_range"

def fetch_cpu_usage(container="load-generator"):
    end=datetime.now()
    start=end-timedelta(minutes=10) #last 10 minutes

    query=f'rate(container_cpu_usage_seconds_total{{container="{container}"}}[30s])'

    params={
        "query": query,
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": "30"
    }

    response=requests.get(PROMETHEUS, params=params).json()
    result=response["data"]["result"]

    if not result:
        print("No data found!")
        return None
    
    timestamps, values=[], []

    for t, v in result[0]['values']:
        timestamps.append(datetime.fromtimestamp(float(t)))
        values.append(float(v))
    
    df = pd.DataFrame({"timestamp": timestamps, "cpu_usage": values})
    df.to_csv("cpu_metrics.csv", index=False)

    print("CPU metrics saved → cpu_metrics.csv")
    return df

if __name__ == "__main__":
    fetch_cpu_usage()