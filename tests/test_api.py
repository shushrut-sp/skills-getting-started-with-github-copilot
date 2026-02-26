from urllib.parse import quote


def test_get_activities(client):
    # Arrange: nothing special, using default snapshot state
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_appears(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    get = client.get("/activities")
    assert email in get.json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "dup@example.com"

    # Act: first signup
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act: duplicate signup
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert r2.status_code == 400


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "remove@example.com"
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act
    r2 = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert r2.status_code == 200
    get = client.get("/activities")
    assert email not in get.json()[activity]["participants"]


def test_unregister_not_signed_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "nosuch@example.com"

    # Act
    r = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert r.status_code == 400


def test_unknown_activity_returns_404(client):
    # Arrange
    email = "x@example.com"

    # Act / Assert for POST
    r1 = client.post(f"/activities/{quote('Nope')}/signup", params={"email": email})
    assert r1.status_code == 404

    # Act / Assert for DELETE
    r2 = client.delete(f"/activities/{quote('Nope')}/signup", params={"email": email})
    assert r2.status_code == 404
