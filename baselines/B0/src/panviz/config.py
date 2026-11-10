"""Defaults for the local academic pilot."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Config:
    DATABASE = str(ROOT / "instance" / "panviz.sqlite3")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    MAX_CSV_ROWS = 10000
    SEED_DEMO = True
    DISTRICT_FILTER_ENABLED = False  # CR01; False reproduces functional baseline B0.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
