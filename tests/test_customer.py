
from http.client import OK, UNAUTHORIZED, CREATED, BAD_REQUEST
from flask.testing import FlaskClient
from pytest import mark

from ipet.ext.customer.models import AssocProductCustomer, Customer
from ipet.ext.customer.schemas import STATUS_CHOICE



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

def test_return_code_customer_products(authentication, client: FlaskClient):
    assert client.get("/customer/1/product", headers=authentication, follow_redirects=True).status_code == OK

def test_customer_products(authentication, client: FlaskClient):
    json = client.get("/customer/1/product", headers=authentication, follow_redirects=True).get_json()
    assert len(json["data"]["elements"]) > 0

def test_authentication_obligation_in_customer_products(client: FlaskClient):
    assert client.get("/customer/1/product", follow_redirects=True).status_code == UNAUTHORIZED

def test_return_code_product_and_customer_information(authentication, client: FlaskClient):
    assert client.get("/customer/1/product/1", headers=authentication, follow_redirects=True).status_code == OK

def test_product_and_customer_information(authentication, client: FlaskClient):
    json = client.get("/customer/1/product/1", headers=authentication, follow_redirects=True).get_json()
    data = json["data"]
    assert bool(data.get("customer")) and bool(data.get("product")) and data["currentStatus"] in STATUS_CHOICE

def test_authentication_obligation_in_product_and_customer_information(client: FlaskClient):
    assert client.get("/customer/1/product/1", follow_redirects=True).status_code == UNAUTHORIZED

@mark.parametrize("status", STATUS_CHOICE)
def test_return_code_update_customer_product_status(authentication, client: FlaskClient, status):
    assert client.patch("/customer/1/product/1", headers=authentication, json={"currentStatus": status}, follow_redirects=True).status_code == OK
    
@mark.parametrize("status", ["IN PROGRESS", "CLOSED", "OPEN"])
def test_return_code_update_customer_product_status(authentication, client: FlaskClient, status):
    assert client.patch("/customer/1/product/1", headers=authentication, json={"currentStatus": status}, follow_redirects=True).status_code == BAD_REQUEST

def test_update_customer_product_status(authentication, client: FlaskClient):
    client.patch("/customer/1/product/1", headers=authentication, json={"currentStatus": "BLOCKED"}, follow_redirects=True).get_json()
    assc = AssocProductCustomer.query.filter(AssocProductCustomer.customer_id==1, AssocProductCustomer.product_id==1).first()
    assert assc.current_status == "BLOCKED"

def test_authentication_obligation_in_update_customer_product_status(client: FlaskClient):
    assert client.patch("/customer/1/product/1", json={"currentStatus": "ACTIVE"}, follow_redirects=True).status_code == UNAUTHORIZED

