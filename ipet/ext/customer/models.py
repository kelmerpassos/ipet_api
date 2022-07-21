"""Module containing customer domain data models."""
from ipet.ext.db import db
from ipet.ext.db.mixins import ManagementMixin


class Customer(db.Model, ManagementMixin):
    """Customer data model."""

    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.BigInteger, nullable=False, unique=True)
    full_name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    products = db.relationship(
        "AssocProductCustomer", back_populates="customer", cascade="all, delete"
    )


class AssocProductCustomer(db.Model, ManagementMixin):
    """Associate Product to Customer."""

    __tablename__ = "inst_product_customer"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    current_status = db.Column(db.String, nullable=False, default="ACTIVE")
    created_at = db.Column(db.DateTime, nullable=False)
    customer = db.relationship("Customer", back_populates="products")
    product = db.relationship("Product")
