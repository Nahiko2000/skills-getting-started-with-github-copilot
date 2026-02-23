import pytest
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_activities_async(async_client):
    # Arrange: none required (use initial data)

    # Act
    resp = await async_client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_and_unregister_async(async_client):
    # Arrange
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    email = "test-async@example.com"

    # Act: signup
    r1 = await async_client.post(f"/activities/{encoded}/signup", params={"email": email})
    # Assert signup succeeded
    assert r1.status_code == 200

    # Act: verify added
    resp = await async_client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Act: unregister
    r2 = await async_client.delete(f"/activities/{encoded}/unregister", params={"email": email})
    # Assert unregister succeeded and removed
    assert r2.status_code == 200
    resp2 = await async_client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]
