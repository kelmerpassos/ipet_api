
from http.client import OK, UNAUTHORIZED, CREATED
from flask.testing import FlaskClient

from ipet.ext.customer.models import Customer



def test_customer_listing_return_code(authentication, client: FlaskClient):
    assert client.get("/customer", headers=authentication, follow_redirects=True).status_code == OK

def test_customer_listing(authentication, client: FlaskClient):
    json = client.get("/customer", headers=authentication, follow_redirects=True).get_json()
    assert len(json["data"]["elements"]) > 0
    
def test_customer_pagination(authentication, client: FlaskClient):
    json = client.get("/customer", headers=authentication, follow_redirects=True).get_json()
    data = json["data"]
    assert "totalPages" in data.keys() and "totalItems" in data.keys() and "currentPage" in data.keys()

def test_authentication_obligation_in_customer_listing(client: FlaskClient):
    assert client.get("/customer", follow_redirects=True).status_code == UNAUTHORIZED

def test_customer_return_code_by_id(authentication, client: FlaskClient):
    assert client.get("/customer/1", headers=authentication, follow_redirects=True).status_code == OK

def test_customer_by_id(authentication, client: FlaskClient):
    json = client.get("/customer/1", headers=authentication, follow_redirects=True).get_json()
    assert bool(json["data"])

def test_authentication_obligation_in_customer_by_id(client: FlaskClient):
    assert client.get("/customer/1", follow_redirects=True).status_code == UNAUTHORIZED

def test_customer_return_code_by_id(authentication, client: FlaskClient):
    assert client.get("/customer/1", headers=authentication, follow_redirects=True).status_code == OK

def test_customer_by_id(authentication, client: FlaskClient):
    json = client.get("/customer/1", headers=authentication, follow_redirects=True).get_json()
    assert bool(json["data"])

def test_authentication_obligation_in_customer_by_id(client: FlaskClient):
    assert client.get("/customer/1", follow_redirects=True).status_code == UNAUTHORIZED

def test_return_code_create_customer(authentication, client: FlaskClient, customer_json):
    assert client.post("/customer", json=customer_json, headers=authentication, follow_redirects=True).status_code == CREATED

def test_create_customer(authentication, client: FlaskClient, customer_json):
    client.post("/customer", json=customer_json, headers=authentication, follow_redirects=True)
    assert Customer.query.filter(Customer.cpf==11111111111).first() is not None

def test_authentication_obligation_in_create_customer(client: FlaskClient, customer_json):
    assert client.post("/customer", json=customer_json, follow_redirects=True).status_code == UNAUTHORIZED

def test_return_code_update_customer(authentication, client: FlaskClient, customer_json):
    assert client.put("/customer/1", json=customer_json, headers=authentication, follow_redirects=True).status_code == OK

def test_update_customer(authentication, client: FlaskClient, customer_json):
    client.put("/customer/1", json=customer_json, headers=authentication, follow_redirects=True)
    assert Customer.query.filter(Customer.cpf==11111111111).first() is not None

def test_authentication_obligation_in_update_customer(client: FlaskClient, customer_json):
    assert client.put("/customer/1", json=customer_json, follow_redirects=True).status_code == UNAUTHORIZED

def test_return_code_partially_update_customer(authentication, client: FlaskClient, customer_json):
    customer_json.pop("cpf")
    assert client.patch("/customer/1", json=customer_json, headers=authentication, follow_redirects=True).status_code == OK

def test_partially_update_customer(authentication, client: FlaskClient, customer_json):
    customer_json.pop("cpf")
    retorno = client.patch("/customer/1", json=customer_json, headers=authentication, follow_redirects=True)
    assert Customer.query.filter(Customer.full_name=="testing").first() is not None

def test_authentication_obligation_in_partially_update_customer(client: FlaskClient, customer_json):
    assert client.patch("/customer/1", json=customer_json, follow_redirects=True).status_code == UNAUTHORIZED

def test_return_code_delete_customer(authentication, client: FlaskClient):
    assert client.delete("/customer/1", headers=authentication, follow_redirects=True).status_code == OK

def test_delete_customer(authentication, client: FlaskClient):
    client.delete("/customer/1", headers=authentication, follow_redirects=True)
    assert Customer.query.get(1) is None

def test_authentication_obligation_in_delete_customer(client: FlaskClient):
    assert client.delete("/customer/1", follow_redirects=True).status_code == UNAUTHORIZED
