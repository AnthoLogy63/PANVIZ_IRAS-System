"""Reproducible digest of runtime, contracts, scripts and tests."""
import hashlib
from pathlib import Path

def source_fingerprint(root):
    root = Path(root)
    files = [root / name for name in ("run.py", "requirements.txt", "pyproject.toml")]
    for folder in ("src", "tests", "datos/entrada", "scripts"):
        files.extend(item for item in (root / folder).rglob("*") if item.is_file() and "__pycache__" not in item.parts)
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda p: p.relative_to(root).as_posix()):
        digest.update(item.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\x00")
        digest.update(item.read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()
