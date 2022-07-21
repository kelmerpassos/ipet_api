from flask.testing import FlaskClient
from http.client import BAD_REQUEST, OK, CREATED, UNAUTHORIZED
from ipet.ext.auth.models import User


def test_post_without_body_in_create_user_resouce(client:FlaskClient):
    assert client.post("/auth", follow_redirects=True).status_code == BAD_REQUEST

def test_return_code_on_user_creation(create_user_response):
    assert create_user_response.status_code == CREATED

def test_user_creation(create_user_response):
    assert User.query.filter(User.username=="testing").first() is not None

def test_return_code_for_user_authentication(authenticate_response):
    authenticate_response.status_code == OK

def test_authentication_return(authenticate_response):
    json = authenticate_response.get_json()
    assert "token" in json.keys() and "refresh_token" in json.keys()

def test_token_refresh_return_code(authentication_refresh, client: FlaskClient):
    assert client.post("/auth/token/refresh", headers=authentication_refresh, follow_redirects=True).status_code == OK

def test_token_update(authentication_refresh, client: FlaskClient):
    json = client.post("/auth/token/refresh", headers=authentication_refresh, follow_redirects=True).get_json()
    assert "token" in json.keys()

def test_token_invalidation_return_code(authentication, client: FlaskClient):
    assert client.post("/auth/token/invalidate", headers=authentication, follow_redirects=True).status_code == OK

def test_token_invalidation(authentication, client: FlaskClient):
    client.post("/auth/token/invalidate", headers=authentication, follow_redirects=True)
    assert client.post("/auth/token/invalidate", headers=authentication, follow_redirects=True).status_code == UNAUTHORIZED