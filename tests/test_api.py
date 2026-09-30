from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_valid_file():
    logs = """2026-10-01 09:00:00 ERROR database-service Connection lost
2026-10-01 09:00:05 INFO auth-service User logged in
2026-10-01 09:00:10 ERROR database-service Query timeout
2026-10-01 09:00:15 WARN payment-service Slow response
2026-10-01 09:00:20 FATAL database-service Database unavailable
2026-10-01 09:00:25 ERROR payment-service Payment failed
invalid log entry"""

    response = client.post(
        "/analyze",
        files={"file": ("test.txt", logs, "text/plain")}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total_lines"] == 7
    assert result["unparseable_lines"] == 1
    assert result["error_count_per_service"] == {
        "auth-service": 0,
        "database-service": 3,
        "payment-service": 1
    }
    assert result["top_offender"] == "database-service"


def test_invalid_file():
    response = client.post(
        "/analyze",
        files={"file": ("test.csv", "some,data", "text/csv")}
    )

    assert response.status_code == 400