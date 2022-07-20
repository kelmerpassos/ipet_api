"""Module that registers customer routes."""
from flask import Blueprint
from flask_restful import Api

from ipet.ext.customer.resources import (
    CustomerListResource,
    CustomerResource,
    ProdsByCustumerResource,
    ProductCustomerResource,
)


def register_routes(bp: Blueprint):
    """Register packet routes.

    Args:
        bp (Blueprint): Package blueprint instance.
    """
    api = Api(bp)
    api.add_resource(CustomerListResource, "/")
    api.add_resource(CustomerResource, "/<int:id>")
    api.add_resource(ProdsByCustumerResource, "/<int:id>/product")
    api.add_resource(ProductCustomerResource, "/<int:id>/product/<int:product_id>")
