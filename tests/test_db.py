import pytest
from sqlalchemy.exc import IntegrityError
from main import db, Destination

def test_create_destination(app_context):    #creating fresh in memory SQLite database and creates destination object like row and adds it to db session
    d = Destination(destination="Paris", country="France", rating=4.7)
    db.session.add(d)
    db.session.commit()

    assert d.id is not None  # auto-generated primary key


def test_read_destination(app_context):  #Inserts Tokyo into DB,Queries the DB: “Give me the row where destination is Tokyo”,This proves your querying + ORM mapping works.
    d = Destination(destination="Tokyo", country="Japan", rating=4.9)
    db.session.add(d)
    db.session.commit()

    found = Destination.query.filter_by(destination="Tokyo").first()
    assert found is not None
    assert found.country == "Japan"
    assert found.rating == 4.9


def test_update_destination(app_context):   #Inserts NYC with rating 4.0,Changes the object in Python to 4.8,Commits again (DB update happens),Reads it again from DB,Confirms rating became 4.8
    d = Destination(destination="NYC", country="USA", rating=4.0)
    db.session.add(d)
    db.session.commit()

    d.rating = 4.8
    db.session.commit()

    updated = db.session.get(Destination, d.id)
    assert updated.rating == 4.8

#Inserts Rome,Stores the ID,Deletes that row,Commits deletion,Tries to fetch it again,Expects None (meaning it is gone)
def test_delete_destination(app_context):
    d = Destination(destination="Rome", country="Italy", rating=4.2)
    db.session.add(d)
    db.session.commit()
    dest_id = d.id

    db.session.delete(d)
    db.session.commit()

    deleted = db.session.get(Destination, dest_id)
    assert deleted is None

#checks the integrity error
def test_not_null_constraints(app_context):
    # destination is nullable=False so this should fail
    bad = Destination(destination=None, country="India", rating=4.5)
    db.session.add(bad)

    with pytest.raises(IntegrityError):
        db.session.commit()

    # Important: rollback after failed commit so session is usable again
    db.session.rollback()
