"""Module that implements serialization and validation of data referring to the product's domain."""
from marshmallow import ValidationError, validates_schema

from ipet.ext.libs import ma
from ipet.ext.libs.ma_schemas import PaginateQueryParamsSchema, ResponsePaginateSchema
from ipet.ext.product.models import Product


class ProductSchema(ma.SQLAlchemySchema):
    """Product data schema."""

    class Meta:
        """Configure class metadata."""

        model = Product
        load_instance = True

    full_name = ma.auto_field(data_key="fullName")
    full_description = ma.auto_field(data_key="fullDescription")
    price = ma.auto_field(as_string=True)
    created_at = ma.auto_field(dump_only=True, data_key="createdAt")
    brand = ma.auto_field()

    @validates_schema
    def validate_names(self, data, **kwargs):
        """Ensure that there is no duplication of full_name and full_description simultaneously."""
        if (
            self.context.get("custom_validate")
            and Product.query.filter(
                Product.full_name == data["full_name"],
                Product.full_description == data["full_description"],
            ).first()
        ):
            raise ValidationError("There is a product with that name and description")


class ProductListSchema(ResponsePaginateSchema):
    """Data schema for product list."""

    elements = ma.List(ma.Nested(ProductSchema))


class ProductsQuerySchema(PaginateQueryParamsSchema):
    """Data schema for query params, used in product queries that require pagination."""

    full_name = ma.String(missing=None, description="Full product name")
    brand = ma.String(missing=None, description="Product brand")
