from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@app.get("/")
def read_root():
    return JSONResponse({"status": "ok", "message": "Cherry Backend is running!"})

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Пересылаем команду всем, КРОМЕ того, кто её отправил
            for connection in manager.active_connections:
                if connection != websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
