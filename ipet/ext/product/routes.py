"""Module that registers product routes."""
from flask import Blueprint
from flask_restful import Api

from ipet.ext.product.resources import ProductListResource, ProductResource


def register_routes(bp: Blueprint):
    """Register packet routes.

    Args:
        bp (Blueprint): Package blueprint instance.
    """
    api = Api(bp)
    api.add_resource(ProductResource, "/<int:id>")
    api.add_resource(ProductListResource, "/")
