def test_create_booking_requires_auth(create_user_and_token):
    client = create_user_and_token["client"]
    payload = {
        "user_id": 1,
        "property_id": 1,
        "start_date": "2025-12-15",
        "end_date": "2025-12-20",
        "total_amount": 100.00
    }
    r = client.post("/api/bookings", json=payload)
    assert r.status_code in (401, 422)


def test_create_booking_with_token(create_user_and_token):
    client = create_user_and_token["client"]
    headers = create_user_and_token["headers"]
    user_id = create_user_and_token["user"]["id"]

    # find a property to book
    rp = client.get("/api/properties")
    assert rp.status_code == 200
    props = rp.json()
    assert props, "No properties available to book"
    prop_id = props[0]["id"]

    payload = {
        "user_id": user_id,
        "property_id": prop_id,
        "start_date": "2025-12-15",
        "end_date": "2025-12-20",
        "total_amount": 500.00
    }
    r = client.post("/api/bookings", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["property_id"] == prop_id
    assert data["user_id"] == user_id
