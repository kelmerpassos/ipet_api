"""Product resource module."""
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from ipet.common.generics.resource import CRUDListResource, CRUDResource
from ipet.ext.product.models import Product
from ipet.ext.product.schemas import (
    ProductListSchema,
    ProductSchema,
    ProductsQuerySchema,
)


class ProductListResource(Resource, CRUDListResource):
    """Resource corresponding to Product collection."""

    def __init__(self) -> None:
        """Initialize properties needed by generic CRUD functions."""
        super().__init__()
        self.ClassModel = Product
        self.ClassSchema = ProductSchema
        self.ClassSchemaList = ProductListSchema
        self.QuerySchema = ProductsQuerySchema
        self.filter = {
            "full_name": self.ClassModel.full_name,
            "brand": self.ClassModel.brand,
        }
        self.order_by = self.ClassModel.id

    @jwt_required()
    def get(self):
        """Get a product list.

        ---
        tags:
        - Product
        summary: Get a product list
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: query
            schema: ProductsQuerySchema
        responses:
            400, 500:
                description: Bad Request, Internal Error
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
        return super().get()

    @jwt_required()
    def post(self):
        """Create a product.

        ---
        tags:
        - Product
        summary: Create a product
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: body
            schema: ProductSchema
        responses:
            400:
                description: '{"message": ""}'
            201:
                description: Returns a complete Product object
                schema:
                    type: object
                    properties:
                        data: ProductSchema
        """
        return super().post()


class ProductResource(Resource, CRUDResource):
    """Resource corresponding to the Product model."""

    def __init__(self) -> None:
        """Initialize properties needed by generic CRUD functions."""
        super().__init__()
        self.ClassModel = Product
        self.ClassSchema = ProductSchema

    @jwt_required()
    def get(self, id: int):
        """Get a product by id.

        ---
        tags:
        - Product
        summary: Get a product by id
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
        responses:
            404, 400, 500:
                description: Product Not Found, Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete Product object
                schema:
                    type: object
                    properties:
                        data: ProductSchema
        """
        return super().get(id)

    @jwt_required()
    def put(self, id: int):
        """Update a product.

        ---
        tags:
        - Product
        summary: Update a product
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
          - in: body
            schema: ProductSchema
        responses:
            404, 400, 500:
                description: Product Not Found, Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete and updated Product object
                schema:
                    type: object
                    properties:
                        data: ProductSchema
        """
        return super().put(id)

    @jwt_required()
    def patch(self, id: int):
        """Partial update a product.

        ---
        tags:
        - Product
        summary: Partially update a product
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
          - in: body
            schema: ProductSchema
        responses:
            404, 400, 500:
                description: Product Not Found, Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns a complete and updated Product object
                schema:
                    type: object
                    properties:
                        data: ProductSchema
        """
        return super().patch(id)

    @jwt_required()
    def delete(self, id: int):
        """Delete a product.

        ---
        tags:
        - Product
        summary: Delete a product
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
          - in: path
            schema: DetailUrlParamSchema
        responses:
            200, 404, 400, 500:
                description: Product deleted, Product Not Found, Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
        """
        return super().delete(id)
