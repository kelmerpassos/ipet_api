"""Module that registers authentication routes."""
from flask import Blueprint
from flask_restful import Api

from ipet.ext.auth.resources import (
    CreateUserResource,
    InvalidateTokenResource,
    RefreshTokenResource,
    TokenResource,
)


def register_routes(bp: Blueprint):
    """Register packet routes.

    Args:
        bp (Blueprint): Package blueprint instance.
    """
    api = Api(bp)
    api.add_resource(CreateUserResource, "/")
    api.add_resource(TokenResource, "/token")
    api.add_resource(RefreshTokenResource, "/token/refresh")
    api.add_resource(InvalidateTokenResource, "/token/invalidate")
