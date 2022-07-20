"""Generic schema module to be used and inherited."""
from marshmallow import validate

from ipet.ext.libs import ma


class PaginateQueryParamsSchema(ma.Schema):
    """Data schema for query parameters, used as pagination edit."""

    page = ma.Integer(
        missing=1,
        description="Paging page number, the first page is 1.",
        validate=validate.Range(min=1),
        required=False,
    )
    per_page = ma.Integer(
        missing=20,
        description="Paging items per page, default 20.",
        validate=validate.Range(min=1, max=50),
        required=False,
    )


class ResponsePaginateSchema(ma.Schema):
    """Data schema for pagination."""

    current_page = ma.Integer(data_key="currentPage")
    total_pages = ma.Integer(data_key="totalPages")
    total_items = ma.Integer(data_key="totalItems")


class DetailUrlParamSchema(ma.Schema):
    """Data schema for URL params by identificator."""

    id = ma.Integer(required=True, description="Identifier Number")
