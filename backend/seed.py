from models import CheckType, Service, SessionLocal, init_db


def run():
    init_db()
    db = SessionLocal()
    try:
        # wipe existing services (safe during early development)
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
                # Service(name="Local TCP", check_type=CheckType.TCP, target="127.0.0.1:5432"),
            ]
        )
        db.commit()
        print("Seeded 2 sample services.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
