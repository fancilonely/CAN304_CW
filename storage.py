# storage.py
"""
SQLite-based one-time usage state manager.

This version persists used message IDs into a local SQLite database file,
so replay / reuse can still be detected across different program runs.
"""

import sqlite3
import time
from pathlib import Path

DB_FILE = "used_messages.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection."""
    return sqlite3.connect(DB_FILE)


def init_storage() -> None:
    """
    Initialize the SQLite database and create the used_messages table if needed.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS used_messages (
            message_id TEXT PRIMARY KEY,
            used_at INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def is_message_used(message_id: str) -> bool:
    """Return True if the message has already been consumed."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM used_messages WHERE message_id = ?",
        (message_id,)
    )
    row = cur.fetchone()

    conn.close()
    return row is not None


def mark_message_used(message_id: str) -> None:
    """Mark a message as consumed."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO used_messages (message_id, used_at) VALUES (?, ?)",
        (message_id, int(time.time()))
    )

    conn.commit()
    conn.close()


def reset_used_messages() -> None:
    """
    Clear all one-time usage records.
    Mainly for testing/demo.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM used_messages")

    conn.commit()
    conn.close()


def get_used_message_count() -> int:
    """Return number of consumed messages currently stored."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM used_messages")
    count = cur.fetchone()[0]

    conn.close()
    return count


def storage_exists() -> bool:
    """Return True if the SQLite database file already exists."""
    return Path(DB_FILE).exists()