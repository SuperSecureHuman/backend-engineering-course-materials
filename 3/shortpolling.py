from fastapi import FastAPI
from uuid import uuid4
from time import time, sleep

app = FastAPI()

# Dictionary to keep track of jobs and their statuses
jobs = {}


@app.post("/start_job")
def start_job(wait_time: int = 10):
    job_id = str(uuid4())
    start_time = time()
    jobs[job_id] = {
        'status': 'in progress',
        'start_time': start_time,
        'wait_time': wait_time
    }
    return {"job_id": job_id}


@app.get("/check_job/{job_id}")
def check_job(job_id: str):
    if job_id not in jobs:
        return {"status": "error", "message": "Job ID not found"}

    job = jobs[job_id]
    if time() < job['start_time'] + job['wait_time']:
        return {"status": "in progress"}
    else:
        jobs[job_id][
            'status'] = 'completed'  # Update the job status to completed
        return {"status": "completed"}
    