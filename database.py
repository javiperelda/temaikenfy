from pathlib import Path
import sqlite3
from dotenv import load_dotenv
import os

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


def get_connection():
    APP_DIR = Path(os.getenv("TEMAIKENFY_DB_PATH"))
    APP_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = APP_DIR / os.getenv("TEMAIKENFY_DB_NAME")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_tokens (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                access_token TEXT NOT NULL,
                token_type TEXT DEFAULT 'Bearer',
                expires_in REAL NOT NULL,
                refresh_token TEXT,
                scope TEXT,
                expires_at REAL NOT NULL,
                feccre TEXT DEFAULT CURRENT_TIMESTAMP,
                fecupd TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS command_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_name TEXT NOT NULL,
                command_text TEXT NOT NULL,
                params_json TEXT,
                status TEXT NOT NULL,
                error_message TEXT,
                executed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

def save_auth_token(access_token, refresh_token, expires_in, expires_at, scope=None, token_type="Bearer"):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO auth_tokens (
                id,
                access_token,
                token_type,
                refresh_token,
                expires_in,
                scope,
                expires_at,
                feccre,
                fecupd                       
            )
            VALUES (1, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                access_token = excluded.access_token,
                token_type = excluded.token_type,
                refresh_token = COALESCE(excluded.refresh_token, auth_tokens.refresh_token),
                expires_in = excluded.expires_in,
                scope = excluded.scope,
                expires_at = excluded.expires_at,
                feccre = CURRENT_TIMESTAMP,     
                fecupd = CURRENT_TIMESTAMP                       
        """, (
            access_token,
            token_type,
            refresh_token,
            expires_in,
            scope,
            expires_at,
        ))

        conn.commit()        

def load_auth_token():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                access_token,
                token_type
                refresh_token,
                expires_in,
                scope,
                expires_at
            FROM auth_tokens
            WHERE id = 1
        """)

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)        