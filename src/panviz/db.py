"""SQLite connections scoped to requests; SQL values are always bound."""
import sqlite3
from pathlib import Path
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS batches (
 id INTEGER PRIMARY KEY, filename TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
 accepted INTEGER NOT NULL, rejected INTEGER NOT NULL, source TEXT NOT NULL DEFAULT 'upload'
);
CREATE TABLE IF NOT EXISTS notifications (
 id TEXT PRIMARY KEY COLLATE NOCASE, fecha_notificacion TEXT NOT NULL,
 establecimiento TEXT NOT NULL, distrito TEXT NOT NULL, grupo_etario TEXT NOT NULL,
 evento TEXT NOT NULL CHECK(evento='IRAS'), semana_iso TEXT NOT NULL,
 batch_id INTEGER NOT NULL REFERENCES batches(id)
);
CREATE TABLE IF NOT EXISTS rejections (
 id INTEGER PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id),
 row_number INTEGER NOT NULL, notification_id TEXT NOT NULL, reason TEXT NOT NULL,
 raw_json TEXT NOT NULL, distrito TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS previews (
 token TEXT PRIMARY KEY, filename TEXT NOT NULL, payload BLOB NOT NULL,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_notifications_dimensions ON notifications(distrito, semana_iso);
CREATE INDEX IF NOT EXISTS idx_rejections_batch ON rejections(batch_id);
PRAGMA user_version = 1;
"""

def get_db():
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"], timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        g.db = connection
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    Path(current_app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    get_db().executescript(SCHEMA)
