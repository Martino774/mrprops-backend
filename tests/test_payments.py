def test_create_payment_requires_auth(create_user_and_token):
    client = create_user_and_token["client"]
    payload = {
        "booking_id": 1,
        "amount": 100.00,
        "payment_method": "tarjeta"
    }
    r = client.post("/api/payments", json=payload)
    assert r.status_code in (401, 422)


def test_create_payment_with_token(create_user_and_token):
    client = create_user_and_token["client"]
    headers = create_user_and_token["headers"]
    user_id = create_user_and_token["user"]["id"]

    # create booking first
    rp = client.get("/api/properties")
    assert rp.status_code == 200
    props = rp.json()
    assert props
    prop_id = props[0]["id"]

    booking_payload = {
        "user_id": user_id,
        "property_id": prop_id,
        "start_date": "2025-12-15",
        "end_date": "2025-12-16",
        "total_amount": 120.00
    }
    rb = client.post("/api/bookings", json=booking_payload, headers=headers)
    assert rb.status_code == 200
    booking = rb.json()

    payment_payload = {
        "booking_id": booking["id"],
        "amount": 120.00,
        "payment_method": "tarjeta"
    }
    rp = client.post("/api/payments", json=payment_payload, headers=headers)
    assert rp.status_code == 200
    p = rp.json()
    assert p["booking_id"] == booking["id"]
    assert float(p["amount"]) == float(payment_payload["amount"]) 
