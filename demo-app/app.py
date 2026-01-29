from fastapi import FastAPI
import time
import threading

app=FastAPI()

memory_holder=[] #global memory throughout run time

@app.get("/")
def root():
    return {"status":"Demo app running successfully"}

@app.get("/cpu") #For CPU loads
def cpu_load():
    def burn_cpu():
        end_time=time.time()+10 #current time + 10

        while time.time()<end_time: #CPU stays busy till condition
            pass
    
    thread=threading.Thread(target=burn_cpu) #running it parallel (background)
    thread.start()
    return{"message":"CPU load started for 10 seconds"}

@app.get("/memory") #Memory load
def memory_load():
    for _ in range(10):
        memory_holder.append("X" * 10**6) # ~1mb*10
    return {"message":"Memory usage increased"}

@app.get("/latency") #Response
def latency():
    time.sleep(2)
    return {"message":"Response deplayed by 2 seconds"}