from fastapi import FastAPI, HTTPException
from uuid import uuid4
from time import sleep
from threading import Thread
from typing import Dict

app = FastAPI()
jobs: Dict[str, Dict] = {}


def background_task(job_id: str, wait_time: int):
    # Simulates a long-running task
    sleep(wait_time)
    jobs[job_id]['status'] = 'completed'


@app.post("/start_job")
async def create_job(wait_time: int = 10):
    job_id = str(uuid4())
    # Create a background task that will update the job status after wait_time seconds
    jobs[job_id] = {'status': 'in progress'}
    task = Thread(target=background_task, args=(job_id, wait_time))
    task.start()
    return {"job_id": job_id}


@app.get("/status/{job_id}")
def get_status(job_id: str, wait: bool = True):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    # Long polling implementation
    while wait and jobs[job_id]['status'] == 'in progress':
        sleep(
            1
        )  # Wait for 1 second before checking the job status again, simulating the long poll

    return {"job_id": job_id, "status": jobs[job_id]['status']}
