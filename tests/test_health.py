from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "F&O trading platform API is running." in response.json()["message"]


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["trading_mode"] == "PAPER"


def test_ready_endpoint() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_trading_status_is_paper_only_by_default() -> None:
    response = client.get("/api/trading/status")
    assert response.status_code == 200
    assert response.json()["mode"] == "PAPER"
    assert response.json()["execution_allowed"] is False


def test_broker_status_is_disabled_by_default() -> None:
    response = client.get("/api/broker/status")
    assert response.status_code == 200
    assert response.json()["configured"] is False
    assert response.json()["live_execution_allowed"] is False
