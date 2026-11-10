"""SQLite Database models for Zerix SaaS."""

import sqlite3
import time
from pathlib import Path
from .auth import generate_api_key

DB_PATH = Path("zerix.db")

def init_db():
    """Initializes the database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabel Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at REAL NOT NULL
        )
    """)
    # Tabel API Keys (Bisa lebih dari 1 per user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at REAL NOT NULL,
            FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def create_user(email: str, role: str = 'viewer') -> bool:
    """Creates a new user in the database."""
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
    """Fetches a user by their API key. Used for auth middleware."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.email, u.role FROM users u
        JOIN api_keys k ON u.email = k.email
        WHERE k.api_key = ?
    """, (api_key,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"id": row[0], "email": row[1], "role": row[2]}
    return None

def create_api_key(email: str) -> str:
    """Generates a new API key for a specific user."""
    key = generate_api_key()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_keys (email, api_key, created_at) VALUES (?, ?, ?)", (email, key, time.time()))
    conn.commit()
    conn.close()
    return key

def get_api_keys(email: str) -> list:
    """Fetches all API keys for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT api_key, created_at FROM api_keys WHERE email = ? ORDER BY created_at DESC", (email,))
    rows = cursor.fetchall()
    conn.close()
    return [{"api_key": r[0], "created_at": r[1]} for r in rows]

def delete_api_key(email: str, api_key: str) -> bool:
    """Deletes a specific API key."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM api_keys WHERE email = ? AND api_key = ?", (email, api_key))
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed
