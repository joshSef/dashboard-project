import socket
import time
from datetime import datetime, timezone

import requests

from models import Check, Service, SessionLocal
from settings import CHECK_INTERVAL_SECONDS, DEFAULT_TIMEOUT_SECONDS


def check_http(url: str, expected: int):
    t0 = time.perf_counter()
    try:
        r = requests.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        latency = int((time.perf_counter() - t0) * 1000)
        if r.status_code == expected:
            return "UP", latency, None
        return "DOWN", latency, f"HTTP {r.status_code} != {expected}"
    except Exception as e:
        latency = int((time.perf_counter() - t0) * 1000)
        return "DOWN", latency, str(e)


def check_tcp(host: str, port: int):
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=DEFAULT_TIMEOUT_SECONDS):
            latency = int((time.perf_counter() - t0) * 1000)
            return "UP", latency, None
    except Exception as e:
        latency = int((time.perf_counter() - t0) * 1000)
        return "DOWN", latency, str(e)


def parse_host_port(target: str):
    host, port = target.split(":")
    return host, int(port)


def run():
    db = SessionLocal()
    while True:
        services = db.query(Service).filter(Service.is_active == True).all()
        for s in services:
            if s.check_type.value == "HTTP":
                status, latency, err = check_http(s.target, s.expected_status)
            else:
                host, port = parse_host_port(s.target)
                status, latency, err = check_tcp(host, port)

            db.add(
                Check(
                    service_id=s.id,
                    status=status,
                    latency_ms=latency,
                    error=err,
                    checked_at=datetime.now(timezone.utc),
                )
            )
            db.commit()
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
