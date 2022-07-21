from http.client import CREATED, OK, UNAUTHORIZED

from flask.testing import FlaskClient

from ipet.ext.product.models import Product


def test_product_listing_return_code(authentication, client: FlaskClient):
    assert (
        client.get(
            "/product", headers=authentication, follow_redirects=True
        ).status_code
        == OK
    )


def test_product_listing(authentication, client: FlaskClient):
    json = client.get(
        "/product", headers=authentication, follow_redirects=True
    ).get_json()
    assert len(json["data"]["elements"]) > 0


def test_product_pagination(authentication, client: FlaskClient):
    json = client.get(
        "/product", headers=authentication, follow_redirects=True
    ).get_json()
    data = json["data"]
    assert (
        "totalPages" in data.keys()
        and "totalItems" in data.keys()
        and "currentPage" in data.keys()
    )


def test_authentication_obligation_in_product_listing(client: FlaskClient):
    assert client.get("/product", follow_redirects=True).status_code == UNAUTHORIZED


def test_product_return_code_by_id(authentication, client: FlaskClient):
    assert (
        client.get(
            "/product/1", headers=authentication, follow_redirects=True
        ).status_code
        == OK
    )


def test_product_by_id(authentication, client: FlaskClient):
    json = client.get(
        "/product/1", headers=authentication, follow_redirects=True
    ).get_json()
    assert bool(json["data"])


def test_authentication_obligation_in_product_by_id(client: FlaskClient):
    assert client.get("/product/1", follow_redirects=True).status_code == UNAUTHORIZED


def test_product_return_code_by_id(authentication, client: FlaskClient):
    assert (
        client.get(
            "/product/1", headers=authentication, follow_redirects=True
        ).status_code
        == OK
    )


def test_product_by_id(authentication, client: FlaskClient):
    json = client.get(
        "/product/1", headers=authentication, follow_redirects=True
    ).get_json()
    assert bool(json["data"])


def test_authentication_obligation_in_product_by_id(client: FlaskClient):
    assert client.get("/product/1", follow_redirects=True).status_code == UNAUTHORIZED


def test_return_code_create_product(authentication, client: FlaskClient, product_json):
    assert (
        client.post(
            "/product", json=product_json, headers=authentication, follow_redirects=True
        ).status_code
        == CREATED
    )


def test_create_product(authentication, client: FlaskClient, product_json):
    client.post(
        "/product", json=product_json, headers=authentication, follow_redirects=True
    )
    assert Product.query.filter(Product.full_name == "Testing").first() is not None


def test_authentication_obligation_in_create_product(client: FlaskClient, product_json):
    assert (
        client.post("/product", json=product_json, follow_redirects=True).status_code
        == UNAUTHORIZED
    )


def test_return_code_update_product(authentication, client: FlaskClient, product_json):
    assert (
        client.put(
            "/product/1",
            json=product_json,
            headers=authentication,
            follow_redirects=True,
        ).status_code
        == OK
    )


def test_update_product(authentication, client: FlaskClient, product_json):
    client.put(
        "/product/1", json=product_json, headers=authentication, follow_redirects=True
    )
    assert Product.query.filter(Product.full_name == "Testing").first() is not None


def test_authentication_obligation_in_update_product(client: FlaskClient, product_json):
    assert (
        client.put("/product/1", json=product_json, follow_redirects=True).status_code
        == UNAUTHORIZED
    )


def test_return_code_partially_update_product(
    authentication, client: FlaskClient, product_json
):
    product_json.pop("fullDescription")
    assert (
        client.patch(
            "/product/1",
            json=product_json,
            headers=authentication,
            follow_redirects=True,
        ).status_code
        == OK
    )


def test_partially_update_product(authentication, client: FlaskClient, product_json):
    product_json.pop("fullDescription")
    client.patch(
        "/product/1", json=product_json, headers=authentication, follow_redirects=True
    )
    assert Product.query.filter(Product.full_name == "Testing").first() is not None


def test_authentication_obligation_in_partially_update_product(
    client: FlaskClient, product_json
):
    assert (
        client.patch("/product/1", json=product_json, follow_redirects=True).status_code
        == UNAUTHORIZED
    )


def test_return_code_delete_product(authentication, client: FlaskClient):
    assert (
        client.delete(
            "/product/1", headers=authentication, follow_redirects=True
        ).status_code
        == OK
    )


def test_delete_product(authentication, client: FlaskClient):
    client.delete("/product/1", headers=authentication, follow_redirects=True)
    assert Product.query.get(1) is None


def test_authentication_obligation_in_delete_product(client: FlaskClient):
    assert (
        client.delete("/product/1", follow_redirects=True).status_code == UNAUTHORIZED
    )
