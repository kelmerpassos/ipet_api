"""Authentication package initialization module."""
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager

from ipet.ext.auth.jwt_callback import register_callbacks
from ipet.ext.auth.routes import register_routes

bp = Blueprint("auth", __name__, url_prefix="/auth")
jwt = JWTManager()
register_callbacks(jwt)
register_routes(bp)


def init_app(app: Flask):
    """Register blueprint in the application.

    Args:
        app (Flask): Aplication instance.
    """
    jwt.init_app(app)
    app.register_blueprint(bp)
