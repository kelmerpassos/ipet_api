"""Module containing product domain data models."""
from ipet.ext.db import db
from ipet.ext.db.mixins import ManagementMixin


class Product(db.Model, ManagementMixin):
    """Product data model."""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    full_description = db.Column(db.String(), nullable=False)
    brand = db.Column(db.String(), nullable=False)
    price = db.Column(db.Numeric(precision=14, scale=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
