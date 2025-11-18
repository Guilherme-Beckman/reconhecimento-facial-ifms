from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import websocket
from fastapi import FastAPI

app = FastAPI()

app.include_router(websocket.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home():
    return HTMLResponse(open("app/static/index.html").read())
