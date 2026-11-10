from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse({"status": "ok", "message": "Cherry Backend is running!"})

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Комната {room_id} получила: {data}")
    except Exception:
        pass
