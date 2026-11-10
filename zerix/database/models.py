"""SQLite Database models for Zerix SaaS."""

import sqlite3
import time
from pathlib import Path

DB_PATH = Path("zerix.db")

def init_db():
    """Initializes the database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_user(email: str, api_key: str, role: str = 'viewer') -> bool:
    """Creates a new user in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, api_key, role, created_at) VALUES (?, ?, ?, ?)",
            (email, api_key, role, time.time())
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False # User or API key already exists

def get_user_by_api_key(api_key: str) -> dict | None:
    """Fetches a user by their API key. Used for auth middleware."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role FROM users WHERE api_key = ?", (api_key,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"id": row[0], "email": row[1], "role": row[2]}
    return None
