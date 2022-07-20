"""Data component initialization module."""
from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_redis = FlaskRedis()


def init_app(app: Flask):
    """Initialize component instances.

    Args:
        app (Flask): Aplication instance.
    """
    db.init_app(app)
    db_redis.init_app(app)
