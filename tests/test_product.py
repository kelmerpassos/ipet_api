
from http.client import OK, UNAUTHORIZED
from flask.testing import FlaskClient


def test_product_listing_return_code(authentication, client: FlaskClient):
    assert client.get("/product", headers=authentication, follow_redirects=True).status_code == OK

def test_product_listing(authentication, client: FlaskClient):
    json = client.get("/product", headers=authentication, follow_redirects=True).get_json()
    assert len(json["data"]["elements"]) > 0
    
def test_product_pagination(authentication, client: FlaskClient):
    json = client.get("/product", headers=authentication, follow_redirects=True).get_json()
    data = json["data"]
    assert "totalPages" in data.keys() and "totalItems" in data.keys() and "currentPage" in data.keys()

def test_authentication_obligation_in_product_listing(client: FlaskClient):
    assert client.get("/product", follow_redirects=True).status_code == UNAUTHORIZED
