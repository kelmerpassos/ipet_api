"""Client package initialization module."""
from flask import Blueprint, Flask

from ipet.ext.customer.routes import register_routes
from ipet.ext.customer.tasks import register_tasks
from ipet.ext.libs import scheduler

bp = Blueprint("customer", __name__, url_prefix="/customer")
register_routes(bp)
register_tasks(scheduler)


def init_app(app: Flask):
    """Register blueprint in the application.

    Args:
        app (Flask): Aplication instance.
    """
    app.register_blueprint(bp)
