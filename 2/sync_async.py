from fastapi import FastAPI
from time import sleep
import httpx
from fastapi.responses import JSONResponse

app = FastAPI()


# Synchronous route
@app.get("/sync")
def read_sync():
    sleep(3)  # Simulate a time-consuming operation
    return {"message": "Hello, world! This is the synchronous route."}


# Asynchronous route
@app.get("/async")
async def read_async():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/delay/3")
        return JSONResponse(content=response.json())
