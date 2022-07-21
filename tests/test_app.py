from http.client import FOUND

from flask.testing import FlaskClient


def test_app_is_created(app):
    assert app.name == "ipet"


def test_root_should_return_status_code_302(client: FlaskClient):
    assert client.get("/").status_code == FOUND


def test_configuration_must_is_enabled(config):
    assert config["TESTING"] == True
