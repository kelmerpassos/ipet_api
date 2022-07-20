"""Module that implements serialization and validation of data referring to the customer's domain."""
from datetime import datetime
from marshmallow import ValidationError, validates
from marshmallow.validate import OneOf, Range

from ipet.ext.customer.models import AssocProductCustomer, Customer
from ipet.ext.libs import ma
from ipet.ext.libs.ma_schemas import PaginateQueryParamsSchema, ResponsePaginateSchema
from ipet.ext.product.schemas import ProductSchema
import re

STATUS_CHOICE = ("ACTIVE", "BLOCKED", "REMOVED")

class CustomerReadSchema(ma.SQLAlchemySchema):
    """Client data schema, load mode (created to solve apispec load_only issue)."""

    class Meta:
        """Configure class metadata."""

        model = Customer

    full_name = ma.auto_field(data_key="fullName")
    created_at = ma.auto_field(data_key="createdAt")


class CustomerSchema(ma.SQLAlchemySchema):
    """Client data schema."""

    class Meta:
        """Configure class metadata."""

        model = Customer
        load_instance = True

    cpf = ma.auto_field(load_only=True, validate=Range(0, 99999999999))
    full_name = ma.auto_field(data_key="fullName")
    created_at = ma.auto_field(dump_only=True, data_key="createdAt")

    @validates("cpf")
    def unique(self, value):
        """Ensure that there is no duplication of CPF."""
        if (
            self.context.get("custom_validate")
            and Customer.query.filter(Customer.cpf == value).first()
        ):
            raise ValidationError("CPF already registered")


class CustomerListSchema(ResponsePaginateSchema):
    """Data schema for customer list."""

    elements = ma.List(ma.Nested(CustomerReadSchema))


class CustomersQuerySchema(PaginateQueryParamsSchema):
    """Data schema for query params, used in customer queries that require pagination."""

    full_name = ma.String(missing=None, description="Full customer name")


class ProductStatusSchema(ma.SQLAlchemySchema):
    """Data schema to change status only. Created for correct view in apispec."""

    class Meta:
        """Configure class metadata."""

        model = AssocProductCustomer
        load_instance = True

    current_status = ma.auto_field(
        data_key="currentStatus", validate=OneOf(STATUS_CHOICE)
    )


class ProductCustomerSchema(ma.SQLAlchemySchema):
    """Data schema that associates product to customer."""

    class Meta:
        """Configure class metadata."""

        model = AssocProductCustomer
        load_instance = True

    product = ma.Nested(ProductSchema)
    customer = ma.Nested(CustomerReadSchema)
    current_status = ma.auto_field(
        data_key="currentStatus", validate=OneOf(STATUS_CHOICE)
    )
    created_at = ma.auto_field(data_key="createdAt")

    @staticmethod
    def normalize_data_list(data: list) -> list:
        """Normalize and validate data in list format.

        Args:
            data (list): Non-serialized data.

        Raises:
            ValueError: Eecord format error.

        Returns:
            list: Serialized data.
        """
        if len(data) != 3:
            raise ValueError(f"Amount of invalid data: {data}")
        normalized_data = [re.sub("[^0-9]", "", d) for d in data]
        if not (normalized_data[0] and normalized_data[1] and len(normalized_data[2])==14):
            raise ValueError(f"Serialized data failure: {normalized_data}")
        try:
            normalized_data[2] = datetime.strptime(normalized_data[2], "%Y%m%d%H%M%S")
        except:
            raise ValueError(f"created_at in invalid format: {normalized_data[2]}")
        return normalized_data

class AssUrlParamSchema(ma.Schema):
    """Data schema for URL params, used in product and customer association."""

    id = ma.Integer(required=True, description="Costumer ID")
    product_id = ma.Integer(required=True, description="Product ID")
