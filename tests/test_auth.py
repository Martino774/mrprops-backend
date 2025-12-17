def test_login_invalid(client):
    r = client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "badpass"})
    assert r.status_code == 401
