from app.monitoring.health import HealthChecker


def test_health_checker_reports_service_status() -> None:
    checker = HealthChecker()
    status = checker.check_all()
    assert "database" in status
    assert "redis" in status
    assert "api" in status
    assert "ai" in status


def test_health_checker_alerts_on_stale_market_data() -> None:
    checker = HealthChecker()
    alert = checker.check_market_data_freshness(age_seconds=600)
    assert alert["status"] == "ALERT"
    assert "stale" in alert["message"].lower()
