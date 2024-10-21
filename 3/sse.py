from fastapi import FastAPI, Response
from typing import Generator
import time

app = FastAPI()


def generate_task_events(task_id: str,
                         duration: int) -> Generator[str, None, None]:
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        time_left = max(end_time - time.time(), 0)
        yield f"data: {{\"task_id\": \"{task_id}\", \"time_left\": {time_left:.0f}}}\n\n"
        time.sleep(1)
    # Task completion event
    yield f"data: {{\"task_id\": \"{task_id}\", \"time_left\": 0}}\n\n"


@app.get("/task/{task_id}")
async def execute_task(task_id: str, response: Response):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    # Example duration of 10 seconds for a task
    return generate_task_events(task_id, duration=10)
