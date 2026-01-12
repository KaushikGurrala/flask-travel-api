import pytest
from main import app, db, Destination


@pytest.fixture()
def client():
    # Use in-memory DB for tests (clean DB every test run)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200


def test_post_and_get_destinations(client):
    # POST
    payload = {"destination": "Paris", "country": "France", "rating": 4.7}
    res = client.post("/destinations", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["destination"] == "Paris"
    assert data["country"] == "France"
    assert data["rating"] == 4.7
    new_id = data["id"]

    # GET all
    res = client.get("/destination")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == new_id


def test_get_by_id(client):
    # Insert directly using ORM
    with app.app_context():
        d = Destination(destination="Tokyo", country="Japan", rating=4.9)
        db.session.add(d)
        db.session.commit()
        dest_id = d.id

    res = client.get(f"/destination/{dest_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["destination"] == "Tokyo"


def test_put_update(client):
    with app.app_context():
        d = Destination(destination="NYC", country="USA", rating=4.0)
        db.session.add(d)
        db.session.commit()
        dest_id = d.id

    res = client.put(f"/destinations/{dest_id}", json={"rating": 4.8})
    assert res.status_code == 200
    data = res.get_json()
    assert data["rating"] == 4.8


def test_delete(client):
    with app.app_context():
        d = Destination(destination="Rome", country="Italy", rating=4.2)
        db.session.add(d)
        db.session.commit()
        dest_id = d.id

    res = client.delete(f"/destinations/{dest_id}")
    assert res.status_code == 200

    # Confirm it's gone
    res = client.get(f"/destination/{dest_id}")
    assert res.status_code == 404
