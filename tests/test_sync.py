from urllib.parse import quote


def test_get_activities(client):
    # Arrange: none required (use initial data)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister_sync(client):
    # Arrange
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    email = "test-sync@example.com"

    # Act: signup
    r1 = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert signup succeeded and participant is present
    assert r1.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act: unregister
    r2 = client.delete(f"/activities/{encoded}/unregister", params={"email": email})

    # Assert unregister succeeded and participant removed
    assert r2.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
