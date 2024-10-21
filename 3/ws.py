from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()
clients: List[WebSocket] = []


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients.append(websocket)

    # Retrieve client's IP address and port number
    client_host = websocket.client.host
    client_port = websocket.client.port

    try:
        # Notify all connected clients including the newly connected one
        for client in clients:
            await client.send_json({
                "message":
                f"User '{client_id}' has connected from IP {client_host} and port {client_port}."
            })

        # Keep the WebSocket connection open and listen for any incoming messages
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        clients.remove(websocket)
        # Notify all connected clients
        for client in clients:
            await client.send_json(
                {"message": f"User '{client_id}' has disconnected."})
    finally:
        # Make sure we clean up if the connection was closed unexpectedly
        if websocket in clients:
            clients.remove(websocket)
