"""Product package initialization module."""
from flask import Blueprint, Flask

from ipet.ext.product.routes import register_routes

bp = Blueprint("product", __name__, url_prefix="/product")
register_routes(bp)


def init_app(app: Flask):
    """Register blueprint in the application.

    Args:
        app (Flask): Aplication instance.
    """
    app.register_blueprint(bp)
