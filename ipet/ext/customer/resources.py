"""Customer resource module."""
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, NotFound

from ipet.common.generics.resource import CRUDListResource, CRUDResource, GetListResorce
from ipet.ext.customer.models import AssocProductCustomer, Customer
from ipet.ext.customer.schemas import (
    CustomerListSchema,
    CustomerSchema,
    CustomersQuerySchema,
    ProductCustomerSchema,
    ProductStatusSchema,
)
from ipet.ext.product.models import Product
from ipet.ext.product.schemas import ProductListSchema, ProductsQuerySchema


class ProductCustomerResource(Resource):
    """Resource corresponding to the AssocProductCustomer model. \
    Contains linked product and customer data."""

    @staticmethod
    def find_element(customer_id, product_id):
        """Get an instance of AssocProductCustomer.

        Args:
            customer_id (int): Customer identifier
            product_id (int): Produts identifier

        Raises:
            NotFound: No element was found with the IDs.

        Returns:
            AssocProductCustomer: Returns an instance of the model
        """
        assoc = AssocProductCustomer.query.filter(
            AssocProductCustomer.customer_id == customer_id,
            AssocProductCustomer.product_id == product_id,
        ).first()
        if not assoc:
            raise NotFound("Element not found")
        return assoc

    @jwt_required()
    def get(self, id, product_id):
        """List product, customer and product status information from an ID product and customer ID.

        ---
        tags:
        - Customer
        summary: Lists product, customer and product status information from an ID product and customer ID
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: AssUrlParamSchema
        responses:
            401, 404, 500:
                description: Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a list of Product objects
                schema:
                    type: object
                    properties:
                        data: ProductCustomerSchema
        """
        assoc = self.find_element(id, product_id)
        return {"data": ProductCustomerSchema().dump(assoc)}

    @jwt_required()
    def patch(self, id, product_id):
        """Change the status of a customer's product.

        ---
        tags:
        - Customer
        summary: Change the status of a customer's product
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: AssUrlParamSchema
          - in: body
            schema: ProductStatusSchema
        responses:
            400, 401, 404, 500:
                description: Bad Request, Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a list of Product objects
                schema:
                    type: object
                    properties:
                        data: ProductCustomerSchema
        """
        assoc = self.find_element(id, product_id)
        json_data = request.get_json()
        try:
            schema = ProductStatusSchema()
            schema.load(json_data, instance=assoc, partial=True)
            assoc.save()
        except ValidationError as error:
            raise BadRequest(error.messages)
        return {"data": schema.dump(assoc)}


class ProdsByCustumerResource(Resource, GetListResorce):
    """Resource that implements product listing by customer."""

    def __init__(self) -> None:
        """Initialize properties needed by generic CRUD functions."""
        super().__init__()
        self.ClassSchemaList = ProductListSchema
        self.QuerySchema = ProductsQuerySchema
        self.filter = {"full_name": Product.full_name, "brand": Product.brand}
        self.order_by = Product.id

    @jwt_required()
    def get(self, id):
        """List products from a customer ID.

        ---
        tags:
        - Customer
        summary: List products from a customer ID
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
          - in: query
            schema: ProductsQuerySchema
        responses:
            401, 404, 500:
                description: Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a list of Product objects
                schema:
                    type: object
                    properties:
                        data: ProductListSchema
        """
        return super().get(
            Product.query.join(AssocProductCustomer)
            .join(Customer)
            .filter(Customer.id == id)
        )


class CustomerListResource(Resource, CRUDListResource):
    """Resource corresponding to Customer collection."""

    def __init__(self) -> None:
        """Initialize properties needed by generic CRUD functions."""
        super().__init__()
        self.ClassModel = Customer
        self.ClassSchemaList = CustomerListSchema
        self.ClassSchema = CustomerSchema
        self.QuerySchema = CustomersQuerySchema
        self.filter = {"full_name": Customer.full_name}
        self.order_by = Customer.id

    @jwt_required()
    def get(self):
        """Get a customer list.

        ---
        tags:
        - Customer
        summary: Get a customer list
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: query
            schema: CustomersQuerySchema
        responses:
            401, 404, 500:
                description: Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a list of Customer objects
                schema:
                    type: object
                    properties:
                        data: CustomerListSchema
        """
        return super().get()

    @jwt_required()
    def post(self):
        """Create a customer.

        ---
        tags:
        - Customer
        summary: Create a customer
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: body
            schema: CustomerSchema
        responses:
            400, 401, 500:
                description: Bad Request, Unautorized, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            201:
                description: Returns a complete Customer object
                schema:
                    type: object
                    properties:
                        data: CustomerReadSchema
        """
        return super().post()


class CustomerResource(Resource, CRUDResource):
    """Resource corresponding to the Customer model."""

    def __init__(self) -> None:
        """Initialize properties needed by generic CRUD functions."""
        super().__init__()
        self.ClassModel = Customer
        self.ClassSchema = CustomerSchema

    @jwt_required()
    def get(self, id: int):
        """Get a customer by id.

        ---
        tags:
        - Customer
        summary: Get a customer by id
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
        responses:
            401, 404, 500:
                description: Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete Customer object
                schema:
                    type: object
                    properties:
                        data: CustomerReadSchema
        """
        return super().get(id)

    @jwt_required()
    def put(self, id: int):
        """Update a customer.

        ---
        tags:
        - Customer
        summary: Update a customer
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
          - in: body
            schema: CustomerSchema
        responses:
            400, 401, 404, 500:
                description:  Bad Request, Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete and updated Customer object
                schema:
                    type: object
                    properties:
                        data: CustomerReadSchema
        """
        return super().put(id)

    @jwt_required()
    def patch(self, id: int):
        """Partial update a customer.

        ---
        tags:
        - Customer
        summary: Partially update a customer
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
          - in: body
            schema: CustomerSchema
        responses:
            400, 401, 404, 500:
                description:  Bad Request, Unautorized, Not Found, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete and updated Customer object
                schema:
                    type: object
                    properties:
                        data: CustomerReadSchema
        """
        return super().patch(id)

    @jwt_required()
    def delete(self, id: int):
        """Delete a customer.

        ---
        tags:
        - Customer
        summary: Delete a customer
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
        responses:
            200, 400, 401, 404, 500:
                description: OK, Bad Request, Not Found, Unautorized, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
        """
        return super().delete(id)
