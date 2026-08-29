import base64
import cv2
import numpy as np
import face_recognition as fr
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.api.routes import websocket
from app.database import (
    salvar_usuario, salvar_auditoria, listar_usuarios, deletar_usuario,
    listar_auditoria, buscar_foto_auditoria, atualizar_status_auditoria,
    aprovar_solicitacao
)

app = FastAPI()
app.include_router(websocket.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class CadastroRequest(BaseModel):
    nome: str
    matricula: str = None
    foto: str

class SolicitacaoRequest(BaseModel):
    nome: str
    matricula: str
    auditoria_id: int

class NovoUsuarioRequest(BaseModel):
    nome: str
    matricula: str
    foto: str
    tipo: str = 'user'

# ── PÁGINAS ───────────────────────────────────────────────

@app.get("/")
def home():
    return HTMLResponse(open("app/static/index.html").read())

@app.get("/cadastro")
def cadastro():
    return HTMLResponse(open("app/static/cadastro.html").read())

@app.get("/admin")
def admin():
    return HTMLResponse(open("app/static/admin.html").read())

# ── SOLICITAÇÃO (usuário comum) ───────────────────────────

@app.post("/solicitar")
def solicitar(req: SolicitacaoRequest):
    try:
        from app.database import atualizar_status_auditoria
        conn = __import__('app.database', fromlist=['get_connection']).get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE auditoria SET nome = %s, matricula = %s, status = 'pendente' WHERE id = %s",
            (req.nome, req.matricula, req.auditoria_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"mensagem": "Solicitação enviada! Aguarde aprovação do administrador."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── ADMIN: listar usuários ────────────────────────────────

@app.get("/api/usuarios")
def get_usuarios():
    return listar_usuarios()

@app.delete("/api/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int):
    try:
        deletar_usuario(usuario_id)
        return {"mensagem": "Usuário deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── ADMIN: auditoria ──────────────────────────────────────

@app.get("/api/auditoria")
def get_auditoria(status: str = None):
    return listar_auditoria(status)

@app.get("/api/auditoria/{auditoria_id}/foto")
def get_foto_auditoria(auditoria_id: int):
    foto = buscar_foto_auditoria(auditoria_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    foto_b64 = base64.b64encode(foto).decode("utf-8")
    return {"foto": foto_b64}

@app.post("/api/auditoria/{auditoria_id}/aprovar")
def aprovar(auditoria_id: int):
    ok, mensagem = aprovar_solicitacao(auditoria_id)
    if not ok:
        raise HTTPException(status_code=400, detail=mensagem)
    return {"mensagem": mensagem}

@app.post("/api/auditoria/{auditoria_id}/rejeitar")
def rejeitar(auditoria_id: int):
    try:
        atualizar_status_auditoria(auditoria_id, 'rejeitado')
        return {"mensagem": "Solicitação rejeitada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── ADMIN: cadastro direto ────────────────────────────────

@app.post("/api/cadastrar")
def cadastrar_direto(req: NovoUsuarioRequest):
    try:
        img_bytes = base64.b64decode(req.foto)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = fr.face_encodings(img_rgb)
        if not encodings:
            raise HTTPException(status_code=400, detail="Nenhum rosto encontrado na foto.")
        salvar_usuario(req.nome, req.matricula, encodings[0], req.tipo)
        return {"mensagem": f"{req.nome} cadastrado com sucesso!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))