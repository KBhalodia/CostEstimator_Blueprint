import sqlite3
import os

DB_PATH = "repair_app.db"

def get_db():
    """Connect to the SQLite database and return a connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name
    return conn

def init_db():
    """Create tables if they don't already exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            item        TEXT NOT NULL,
            condition   TEXT NOT NULL,
            zip         TEXT NOT NULL,
            repair_cost REAL NOT NULL,
            replace_cost REAL NOT NULL,
            verdict     TEXT NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()
    print("✅ Database initialized.")
