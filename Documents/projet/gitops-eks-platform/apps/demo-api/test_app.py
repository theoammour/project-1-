from app import app


def test_healthz():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_index():
    client = app.test_client()
    resp = client.get("/")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["service"] == "demo-api"


def test_metrics_exposed():
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"demo_api_requests_total" in resp.data
