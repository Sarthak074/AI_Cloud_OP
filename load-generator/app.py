from fastapi import FastAPI
import time
import threading

from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse

app = FastAPI()

memory_holder = []  # global memory for demo

# --- Prometheus Metrics ---
CPU_COUNTER = Counter("loadgen_cpu_requests_total", "CPU load requests")
MEMORY_COUNTER = Counter("loadgen_memory_requests_total", "Memory load requests")
LATENCY_HIST = Histogram("loadgen_latency_seconds", "Latency for /latency endpoint")

@app.get("/")
def root():
    return {"status": "Load generator running successfully"}

@app.get("/cpu")
def cpu_load():
    CPU_COUNTER.inc()

    def burn_cpu():
        end_time = time.time() + 10
        while time.time() < end_time:
            pass

    thread = threading.Thread(target=burn_cpu)
    thread.start()
    return {"message": "CPU load started for 10 seconds"}

@app.get("/memory")
def memory_load():
    MEMORY_COUNTER.inc()
    for _ in range(10):
        memory_holder.append("X" * 10**6)
    return {"message": "Memory usage increased"}

@app.get("/latency")
def latency():
    with LATENCY_HIST.time():  # <-- Track latency automatically
        time.sleep(2)
    return {"message": "Response delayed by 2 seconds"}

# --- Required for Prometheus ---
@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")