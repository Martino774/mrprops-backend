def test_list_properties(client):
    r = client.get("/api/properties")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_property_requires_auth(create_user_and_token):
    client = create_user_and_token["client"]
    payload = {
        "title": "Test Property Auth",
        "description": "Test",
        "price": 100.0,
        "location": "Test City",
        "image_url": "https://example.com/img.jpg",
        "property_type": "alquiler",
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 45
    }
    r = client.post("/api/properties", json=payload)
    assert r.status_code in (401, 422)


def test_create_property_with_token(create_user_and_token):
    client = create_user_and_token["client"]
    headers = create_user_and_token["headers"]
    payload = {
        "title": "Test Property From Integration",
        "description": "Test",
        "price": 200.0,
        "location": "Test City",
        "image_url": "https://example.com/img.jpg",
        "property_type": "alquiler",
        "bedrooms": 2,
        "bathrooms": 1,
        "area": 70
    }
    r = client.post("/api/properties", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == payload["title"]


def test_property_has_created_at(client):
    r = client.get("/api/properties")
    assert r.status_code == 200
    if r.json():
        assert "created_at" in r.json()[0]