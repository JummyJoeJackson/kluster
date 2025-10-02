def test_health_endpoints(client):
    assert client.get("/healthz").status_code == 200
    assert client.get("/livez").status_code == 200
    # metrics endpoint exists
    assert client.get("/metrics").status_code == 200
