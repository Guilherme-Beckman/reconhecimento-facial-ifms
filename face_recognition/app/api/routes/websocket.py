from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    ##do something about camera things
