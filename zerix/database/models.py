"""SQLite Database models for Zerix SaaS."""

import sqlite3
import time
import secrets
from pathlib import Path
from .auth import generate_api_key

DB_PATH = Path("zerix.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at REAL NOT NULL,
            FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            expires_at REAL NOT NULL,
            FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def create_user(email: str, role: str = 'viewer') -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, role, created_at) VALUES (?, ?, ?)", (email, role, time.time()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_api_key(api_key: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.email, u.role FROM users u
        JOIN api_keys k ON u.email = k.email
        WHERE k.api_key = ?
    """, (api_key,))
    row = cursor.fetchone()
    conn.close()
    return {"id": row[0], "email": row[1], "role": row[2]} if row else None

def create_api_key(email: str) -> str:
    key = generate_api_key()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_keys (email, api_key, created_at) VALUES (?, ?, ?)", (email, key, time.time()))
    conn.commit()
    conn.close()
    return key

def get_api_keys(email: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT api_key, created_at FROM api_keys WHERE email = ? ORDER BY created_at DESC", (email,))
    rows = cursor.fetchall()
    conn.close()
    return [{"api_key": r[0], "created_at": r[1]} for r in rows]

def delete_api_key(email: str, api_key: str) -> bool:
    """Menghapus API Key, tapi menolak jika itu adalah key terakhir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cek jumlah key yang dimiliki user
    cursor.execute("SELECT COUNT(*) FROM api_keys WHERE email = ?", (email,))
    count = cursor.fetchone()[0]
    
    if count <= 1:
        conn.close()
        return False # Tolak hapus jika hanya sisa 1 key
        
    cursor.execute("DELETE FROM api_keys WHERE email = ? AND api_key = ?", (email, api_key))
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def create_session(email: str) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = time.time() + (7 * 24 * 60 * 60)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (token, email, expires_at) VALUES (?, ?, ?)", (token, email, expires_at))
    conn.commit()
    conn.close()
    return token

def get_user_by_session(token: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.email, u.role, s.expires_at FROM users u
        JOIN sessions s ON u.email = s.email
        WHERE s.token = ?
    """, (token,))
    row = cursor.fetchone()
    if row and row[3] > time.time():
        conn.close()
        return {"id": row[0], "email": row[1], "role": row[2]}
    conn.close()
    return None

def delete_session(token: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()
