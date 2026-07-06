import base64
import cv2
import numpy as np
import face_recognition as fr
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.api.routes import websocket
from app.database import salvar_usuario, salvar_auditoria

app = FastAPI()
app.include_router(websocket.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class CadastroRequest(BaseModel):
    nome: str
    matricula: str = None
    foto: str

@app.get("/")
def home():
    return HTMLResponse(open("app/static/index.html").read())

@app.get("/cadastro")
def cadastro():
    return HTMLResponse(open("app/static/cadastro.html").read())

@app.post("/cadastrar")
def cadastrar(req: CadastroRequest):
    try:
        img_bytes = base64.b64decode(req.foto)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encodings = fr.face_encodings(img_rgb)
        if not encodings:
            raise HTTPException(status_code=400, detail="Nenhum rosto encontrado na foto.")

        salvar_usuario(req.nome, req.matricula, encodings[0])
        salvar_auditoria(img_bytes)

        return {"mensagem": f"{req.nome} cadastrado com sucesso!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))