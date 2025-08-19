from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import desc

from models import Check, Service, SessionLocal, init_db
from settings import ALLOWED_ORIGINS

init_db()
app = FastAPI(title="Dashboard Project API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ServiceOut(BaseModel):
    id: int
    name: str
    check_type: str
    target: str
    latest_status: str | None
    latency_ms: int | None
    checked_at: str | None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/services")
def list_services():
    db = SessionLocal()
    try:
        services = db.query(Service).filter(Service.is_active == True).all()
        result = []
        for s in services:
            last = (
                db.query(Check)
                .filter(Check.service_id == s.id)
                .order_by(desc(Check.checked_at))
                .first()
            )
            result.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "check_type": s.check_type.value,
                    "target": s.target,
                    "latest_status": last.status if last else None,
                    "latency_ms": last.latency_ms if last else None,
                    "checked_at": last.checked_at.isoformat() if last else None,
                }
            )
        return result
    finally:
        db.close()


@app.get("/api/services/{service_id}/checks")
def service_checks(service_id: int, limit: int = 20):
    db = SessionLocal()
    try:
        rows = (
            db.query(Check)
            .filter(Check.service_id == service_id)
            .order_by(desc(Check.checked_at))
            .limit(limit)
            .all()
        )
        return [
            {
                "status": r.status,
                "latency_ms": r.latency_ms,
                "checked_at": r.checked_at.isoformat(),
                "error": r.error,
            }
            for r in rows
        ]
    finally:
        db.close()
