import psycopg2
import numpy as np
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

def carregar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, matricula, encoding FROM usuarios")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    nomes = []
    encodings = []
    for nome, matricula, encoding_bytes in rows:
        nomes.append(nome)
        encodings.append(pickle.loads(encoding_bytes))

    return nomes, encodings

def salvar_usuario(nome, matricula, encoding_array):
    conn = get_connection()
    cur = conn.cursor()
    encoding_bytes = pickle.dumps(encoding_array)
    cur.execute(
        "INSERT INTO usuarios (nome, matricula, encoding) VALUES (%s, %s, %s)",
        (nome, matricula, encoding_bytes)
    )
    conn.commit()
    cur.close()
    conn.close()

def salvar_auditoria(foto_bytes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO auditoria (foto) VALUES (%s) RETURNING id",
        (foto_bytes,)
    )
    auditoria_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return auditoria_id