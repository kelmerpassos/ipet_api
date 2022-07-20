"""OpenAPI initialization and configuration module."""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint, Flask

from ipet.ext.doc.plugins import automatic_mapping
from ipet.ext.doc.routes import register_routes

spec = APISpec(
    title="iPET-api-documentation",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("jwt", jwt_scheme)

bp = Blueprint("doc", __name__, url_prefix="/swagger", template_folder="templates")
register_routes(bp, spec)


def init_app(app: Flask):
    """Register blueprint in the application.

    Args:
        app (Flask): Aplication instance.
    """
    automatic_mapping(spec, app)
    app.register_blueprint(bp)
