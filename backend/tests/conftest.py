import os
import sys
from pathlib import Path

# Point DATABASE_URL to a temporary file first, so models bind to test DB
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

# Make both backend/ and repo root importable
THIS_DIR = Path(__file__).resolve().parent
BACKEND_DIR = THIS_DIR.parent  # .../backend
REPO_ROOT = BACKEND_DIR.parent  # repo root

for p in (str(BACKEND_DIR), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)


import pytest
from fastapi.testclient import TestClient

# Try both import styles, depending on how tests are invoked
try:
    from app import app  # when cwd == backend
except ModuleNotFoundError:
    from backend.app import app  # when cwd == repo root

from models import CheckType, Service, SessionLocal, init_db


@pytest.fixture(autouse=True)
def _fresh_db(tmp_path):
    """Create a fresh SQLite DB file per test session and bind via env."""
    dbfile = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{dbfile}"
    init_db()
    yield
    # SQLite file will live in tmp_path; no explicit teardown needed.


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def seeded_services():
    init_db()
    db = SessionLocal()
    try:
        db.query(Service).delete()
        db.add_all(
            [
                Service(
                    name="API Health",
                    check_type=CheckType.HTTP,
                    target="http://127.0.0.1:8000/health",
                    expected_status=200,
                ),
                Service(
                    name="Bad HTTP",
                    check_type=CheckType.HTTP,
                    target="https://example.com/does-not-exist",
                    expected_status=200,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()
