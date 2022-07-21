from pytest import fixture
from ipet import create_app
from ipet.ext.db import db
from ipet.ext.cli.views import populate_db

@fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        populate_db()
        yield app
        db.drop_all()

@fixture
def create_user_response(client):
    json = {"username": "testing", "password": "testing"}
    return client.post("/auth", json=json, follow_redirects=True)

@fixture
def authenticate_response(client):
    json = {"username":"admin", "password": "admin"}
    return client.post("/auth/token", json=json, follow_redirects=True)

@fixture
def authentication(authenticate_response):
    json = authenticate_response.get_json()
    return {"Authorization": f"Bearer {json['token']}"} 

@fixture
def authentication_refresh(authenticate_response):
    json = authenticate_response.get_json()
    return {"Authorization": f"Bearer {json['refresh_token']}"} 