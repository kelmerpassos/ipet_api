"""Module that initializes libraries."""
from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_marshmallow import Marshmallow

ma = Marshmallow()
cors = CORS(resources={"/*": {"origins": "*"}})
scheduler = APScheduler()


def init_app(app: Flask):
    """Initialize component instances.

    Args:
        app (Flask): Aplication instance.
    """
    ma.init_app(app)
    cors.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
