from flask.testing import FlaskClient
from pytest import fixture

from ipet import create_app
from ipet.ext.cli.views import populate_db
from ipet.ext.db import db


@fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        populate_db()
        yield app
        db.drop_all()


@fixture
def create_user_response(client: FlaskClient):
    json = {"username": "testing", "password": "testing"}
    return client.post("/auth", json=json, follow_redirects=True)


@fixture
def authenticate_response(client: FlaskClient):
    json = {"username": "admin", "password": "admin"}
    return client.post("/auth/token", json=json, follow_redirects=True)


@fixture
def authentication(authenticate_response):
    json = authenticate_response.get_json()
    return {"Authorization": f"Bearer {json['token']}"}


@fixture
def authentication_refresh(authenticate_response):
    json = authenticate_response.get_json()
    return {"Authorization": f"Bearer {json['refresh_token']}"}


@fixture
def product_json():
    return {
        "fullName": "Testing",
        "fullDescription": "testing",
        "price": 90.1,
        "brand": "teste",
    }


@fixture
def customer_json():
    return {"cpf": 11111111111, "fullName": "testing", "address": "rua testing"}
