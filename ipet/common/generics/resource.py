"""Module that creates generic classes to be used in CRUD routines."""
from http.client import CREATED

from flask import request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest, NotFound

from ipet.ext.db.mixins import ManagementMixin


def find_by_id(id, ClassModel):
    """Take, from a generic model, an element.

    Args:
        id (int): Element identifier.
        ClassModel: Data model class.

    Raises:
        NotFound: No element was found with the ID.

    Returns:
        Model instance.
    """
    element = ClassModel.query.get(id)
    if element:
        return element
    raise NotFound("Element not found")


def update(
    id: int, ClassModel, ClassSchema, partial: bool = False, error_msg: str = None
):
    """Update an element from generic model.

    Args:
        id (int): Element identifier.
        ClassModel: Data model class.
        ClassSchema: Data schema class.
        partial (bool, optional): Informs whether to perform a partial update of the element. Defaults to False.
        error_msg (str, optional): Error message to be reported. Defaults to None.

    Raises:
        BadRequest: Error in validating sent data.

    Returns:
        Serialized element.
    """
    element = find_by_id(id, ClassModel)
    json_data = request.get_json()
    try:
        schema = ClassSchema()
        schema.context = {"custom_validate": False}
        schema.load(json_data, instance=element, partial=partial)
        ManagementMixin.save_element(element, error_msg)
    except ValidationError as error:
        raise BadRequest(error.messages)
    return {"data": schema.dump(element)}


class PostResource:
    """Generic class for HTTP POST."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassSchema = None

    def post(self, error_msg: str = None):
        """Save an element, based on generic schema.

        Args:
            error_msg (str, optional): Error message to be reported. Defaults to None.

        Raises:
            BadRequest: Error in validating sent data.

        Returns:
            Serialized element.
        """
        json_data = request.get_json()
        try:
            schema = self.ClassSchema()
            schema.context = {"custom_validate": True}
            element = schema.load(json_data)
        except ValidationError as error:
            raise BadRequest(error.messages)
        ManagementMixin.save_element(element, error_msg)
        return {"data": schema.dump(element)}, CREATED


class PatchResource:
    """Generic class for HTTP PATCH."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchema = None

    def patch(self, id: int):
        """Partial update an element, based on generic schema.

        Args:
            id (int): Element identifier.

        Returns:
            Serialized element.
        """
        return update(id, self.ClassModel, self.ClassSchema, partial=True)


class PutResorce:
    """Generic class for HTTP PUT."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchema = None

    def put(self, id: int):
        """Update an element, based on generic schema.

        Args:
            id (int): Element identifier.

        Returns:
            Serialized element.
        """
        return update(id, self.ClassModel, self.ClassSchema, partial=False)


class GetResorce:
    """Generic class for HTTP GET."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchema = None

    def get(self, id: int):
        """Get information from an element.

        Args:
            id (int): Element identifier.

        Returns:
            Serialized element.
        """
        element = find_by_id(id, self.ClassModel)
        return {"data": self.ClassSchema().dump(element)}


class DeleteResorce:
    """Generic class for HTTP DELETE."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None

    def delete(self, id: int) -> dict:
        """Delete an element.

        Args:
            id (int): Element identifier.

        Returns:
            return message
        """
        element = find_by_id(id, self.ClassModel)
        ManagementMixin.delete(element)
        return {"message": "Element deleted successfully"}


class GetListResorce:
    """Generic class for HTTP GET, in object list."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchemaList = None
        self.QuerySchema = None
        self.filter = {}
        self.order_by = None

    def get(self, query=None):
        """Get information from a list of elements. With pagination.

        Args:
            query (optional): SQLAlchemy query base, used for pre-filtering data. Defaults to None.

        Raises:
            BadRequest: Error in validating sent data.

        Returns:
            Serialized list of elements
        """
        try:
            req_schema = self.QuerySchema().load(request.args)
            per_page = req_schema.pop("per_page")
            page = req_schema.pop("page")
        except ValidationError as error:
            raise BadRequest(error.messages)
        if not query:
            query = self.ClassModel.query
        for key, field in self.filter.items():
            if req_schema.get(key):
                query = query.filter(field.ilike(f"%{req_schema[key]}%"))
        paginate = query.order_by(self.order_by).paginate(
            per_page=per_page,
            page=page,
            error_out=True,
        )
        schema = self.ClassSchemaList()
        data = schema.dump(
            {
                "elements": paginate.items,
                "current_page": paginate.page,
                "total_pages": paginate.pages,
                "total_items": paginate.total,
            }
        )
        return {"data": data}


class CRUDResource(GetResorce, PutResorce, PatchResource, DeleteResorce):
    """HTTP methods condemning class."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchema = None


class CRUDListResource(GetListResorce, PostResource):
    """HTTP methods condemning class."""

    def __init__(self) -> None:
        """Properties to be overwritten."""
        self.ClassModel = None
        self.ClassSchema = None
        self.QuerySchema = None
        self.filter = {}
        self.order_by = None
