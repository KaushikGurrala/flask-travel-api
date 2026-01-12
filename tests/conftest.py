import pytest
from main import app,db

@pytest.fixture()
def app_context():
    #configure app for testing DB
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )


    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


#What this does:

#Uses SQLite in-memory DB

#Creates tables before each test

#Drops everything after each test (clean slate)