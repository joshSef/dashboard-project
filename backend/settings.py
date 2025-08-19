from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env placed in backend/ (fallback: repo root)
_here = Path(__file__).resolve().parent
env_paths = [
    _here / ".env",
    _here.parent / ".env",  # repo root fallback if you prefer
]
for p in env_paths:
    if p.exists():
        load_dotenv(p)
        break

# Defaults that are safe for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./monitor.db")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "30"))
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "3"))

# Allowed web origins (for Vite dev server)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(
    ","
)
