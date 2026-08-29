import psycopg2
import pickle
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "dbname": os.getenv("DB_NAME", "facial_ifms"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "senha123")
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ── USUÁRIOS ──────────────────────────────────────────────

def carregar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, matricula, encoding FROM usuarios")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    nomes, encodings = [], []
    for nome, matricula, encoding_bytes in rows:
        nomes.append(nome)
        encodings.append(pickle.loads(encoding_bytes))
    return encodings, nomes

def salvar_usuario(nome, matricula, encoding_array, tipo='user'):
    conn = get_connection()
    cur = conn.cursor()
    encoding_bytes = pickle.dumps(encoding_array)
    cur.execute(
        "INSERT INTO usuarios (nome, matricula, encoding, tipo) VALUES (%s, %s, %s, %s)",
        (nome, matricula, encoding_bytes, tipo)
    )
    conn.commit()
    cur.close()
    conn.close()

def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, matricula, tipo, criado_em FROM usuarios ORDER BY criado_em DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nome": r[1], "matricula": r[2], "tipo": r[3], "criado_em": str(r[4])} for r in rows]

def deletar_usuario(usuario_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()

def buscar_usuario_por_matricula(matricula):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, tipo FROM usuarios WHERE matricula = %s", (matricula,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

# ── AUDITORIA ─────────────────────────────────────────────

def salvar_auditoria(foto_bytes, status='desconhecido', nome=None, matricula=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO auditoria (foto, status, nome, matricula) VALUES (%s, %s, %s, %s) RETURNING id",
        (foto_bytes, status, nome, matricula)
    )
    auditoria_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return auditoria_id

def listar_auditoria(status=None):
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute("SELECT id, momento, status, nome, matricula FROM auditoria WHERE status = %s ORDER BY momento DESC", (status,))
    else:
        cur.execute("SELECT id, momento, status, nome, matricula FROM auditoria ORDER BY momento DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "momento": str(r[1]), "status": r[2], "nome": r[3], "matricula": r[4]} for r in rows]

def buscar_foto_auditoria(auditoria_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT foto FROM auditoria WHERE id = %s", (auditoria_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return bytes(row[0]) if row else None

def atualizar_status_auditoria(auditoria_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE auditoria SET status = %s WHERE id = %s", (status, auditoria_id))
    conn.commit()
    cur.close()
    conn.close()

def aprovar_solicitacao(auditoria_id):
    """Busca os dados da auditoria, gera o usuário e marca como aprovado."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT foto, nome, matricula FROM auditoria WHERE id = %s", (auditoria_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return False, "Solicitação não encontrada"

    foto_bytes, nome, matricula = bytes(row[0]), row[1], row[2]

    if not nome or not matricula:
        return False, "Solicitação sem nome ou matrícula"

    import numpy as np
    import face_recognition as fr
    import cv2

    img_array = np.frombuffer(foto_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = fr.face_encodings(img_rgb)

    if not encodings:
        return False, "Nenhum rosto encontrado na foto"

    salvar_usuario(nome, matricula, encodings[0])
    atualizar_status_auditoria(auditoria_id, 'aprovado')
    return True, "Usuário cadastrado com sucesso"