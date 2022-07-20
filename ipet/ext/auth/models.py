"""Module containing authentication domain models."""
from ipet.ext.db import db
from ipet.ext.db.mixins import ManagementMixin


class User(db.Model, ManagementMixin):
    """User data model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
