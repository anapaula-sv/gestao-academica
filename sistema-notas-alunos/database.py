import sqlite3
import json
import hashlib

def conectar():
    return sqlite3.connect('escola.db')

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                notas TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()
    
    try:
        if not db_verificar_usuario("admin", "admin123"):
            db_cadastrar_usuario("admin", "admin123")
    except:
        pass

def db_cadastrar_usuario(usuario, senha):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            senha_hash = gerar_hash(senha)
            cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha_hash))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def db_verificar_usuario(usuario, senha):
    with conectar() as conn:
        cursor = conn.cursor()
        senha_hash = gerar_hash(senha)
        cursor.execute('SELECT id FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha_hash))
        row = cursor.fetchone()
        return row is not None

def db_cadastrar_aluno(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO alunos (nome, notas) VALUES (?, ?)', (nome, json.dumps([])))
        conn.commit()

def db_buscar_aluno(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome, notas FROM alunos WHERE nome = ?', (nome,))
        row = cursor.fetchone()
        if row:
            return {"nome": row[0], "notas": json.loads(row[1])}
    return None

def db_atualizar_notas(nome, novas_notas):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE alunos SET notas = ? WHERE nome = ?', (json.dumps(novas_notas), nome))
        conn.commit()

def db_excluir_aluno(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM alunos WHERE nome = ?', (nome,))
        conn.commit()

def db_listar_todos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome, notas FROM alunos')
        rows = cursor.fetchall()
        return [{"nome": r[0], "notas": json.loads(r[1])} for r in rows]


criar_tabelas()