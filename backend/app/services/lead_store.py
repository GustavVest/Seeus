"""
Tiny SQLite-backed lead store.

Single source of truth for captured leads. The /count and /admin/leads
endpoints both read from here; /subscribe writes here. Resend (when
configured) is a downstream fan-out, not the system of record.

Storage path:
    LEADS_DB_PATH env var, default /tmp/leads.db.

    Set LEADS_DB_PATH=/data/leads.db on Railway after attaching a volume
    at /data, and the data survives deploys. Without a volume, /tmp is
    wiped on every deploy — fine for early traffic, but you'll lose the
    history each time the service redeploys.
"""

from __future__ import annotations
import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator


def _db_path() -> str:
    return os.environ.get('LEADS_DB_PATH', '/tmp/leads.db')


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(_db_path(), timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create the leads table if it doesn't exist. Safe to call on every boot."""
    with _connect() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                email      TEXT PRIMARY KEY,
                company    TEXT,
                category   TEXT,
                source     TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        c.commit()


def add_lead(email: str, company: str = '', category: str = '', source: str = 'configurator') -> bool:
    """Insert a lead. Returns True on insert, False on duplicate."""
    email = (email or '').strip().lower()
    if not email:
        return False
    with _connect() as c:
        try:
            c.execute(
                'INSERT INTO leads (email, company, category, source) VALUES (?, ?, ?, ?)',
                (email, company or '', category or '', source or 'configurator'),
            )
            c.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def count_leads() -> int:
    """Return the total number of unique leads captured."""
    with _connect() as c:
        return c.execute('SELECT COUNT(*) FROM leads').fetchone()[0]


def list_leads() -> list[dict]:
    """Return every lead, newest first, as a list of plain dicts."""
    with _connect() as c:
        rows = c.execute(
            'SELECT email, company, category, source, created_at FROM leads ORDER BY created_at DESC'
        ).fetchall()
        return [dict(r) for r in rows]
