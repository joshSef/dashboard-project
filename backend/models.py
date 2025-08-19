import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from settings import DATABASE_URL

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine)


class CheckType(enum.Enum):
    HTTP = "HTTP"
    TCP = "TCP"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    check_type = Column(Enum(CheckType), nullable=False)
    target = Column(String(255), nullable=False)  # URL or host:port
    expected_status = Column(Integer, default=200)  # for HTTP
    is_active = Column(Boolean, default=True)
    checks = relationship("Check", back_populates="service", cascade="all, delete-orphan")


class Check(Base):
    __tablename__ = "checks"
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"), index=True)
    status = Column(String(10))  # "UP" | "DOWN"
    latency_ms = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    checked_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    service = relationship("Service", back_populates="checks")


def init_db():
    Base.metadata.create_all(engine)
