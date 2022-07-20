"""Authentication resource module."""
from datetime import timedelta
from http.client import CREATED, UNAUTHORIZED

from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from werkzeug.security import safe_str_cmp

from ipet.ext.auth.models import User
from ipet.ext.auth.schema import UserSchema
from ipet.ext.config import environment_var
from ipet.ext.db import db_redis


def get_json_user(custom_validate: bool = True):
    """Get an instance of User.

    Args:
        custom_validate (bool, optional): Define whether the schema should use custom validations.
        Defaults to True.

    Raises:
        BadRequest: Error in validating sent data.

    Returns:
        return validated data
    """
    try:
        schema = UserSchema()
        schema.context = {"custom_validate": custom_validate}
        json_data = schema.load(request.get_json())
    except ValidationError as error:
        raise BadRequest(error.messages)
    return json_data


class TokenResource(Resource):
    """Resource that implements token generation routine."""

    def post(self):
        """Generate a token from a registered user.

        ---
        tags:
        - Auth
        summary: Generate a token from a registered user
        parameters:
          - in: body
            schema: UserSchema
        responses:
            400, 500:
                description: Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns access credentials
                schema:
                    type: object
                    properties:
                        data: RefreshTokenSchema
        """
        json_user = get_json_user(False)
        user = User.query.filter_by(username=json_user["username"]).first()
        if user and safe_str_cmp(user.password, json_user["password"]):
            return {
                "token": create_access_token(identity=user),
                "refresh_token": create_refresh_token(identity=user),
            }
        return {
            "message": "Incorrect username or password",
        }, UNAUTHORIZED


class RefreshTokenResource(Resource):
    """Resource that implements token renewal routine by refresh token."""

    @jwt_required(refresh=True)
    def post(self):
        """Generate a token from a refresh token.

        ---
        tags:
        - Auth
        summary: Generate a token from a refresh token
        security:
          - jwt: []
        parameters:
          - in: header
            schema: RefreshAuthSchema
        responses:
            401, 500:
                description: Unautorized, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
            200:
                description: Returns access credentials
                schema:
                    type: object
                    properties:
                        data: SimpleTokenSchema
        """
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {"token": access_token}


class InvalidateTokenResource(Resource):
    """Resource responsible for invalidating token."""

    @jwt_required()
    def post(self):
        """Invalidates a token.

        ---
        tags:
        - Auth
        summary: Invalidates a token
        security:
          - jwt: []
        parameters:
          - in: header
            schema: AuthorizationSchema
        responses:
            200, 401, 500:
                description: Created, Unautorized, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
        """
        db_redis.set(
            get_jwt()["jti"],
            "",
            ex=timedelta(seconds=environment_var.JWT_ACCESS_TOKEN_EXPIRES),
        )
        return {"message": "Successfully invalidated token"}


class CreateUserResource(Resource):
    """Resource corresponding to the User model."""

    def post(self):
        """Create a user.

        ---
        tags:
        - Auth
        summary: Create a user
        parameters:
          - in: body
            schema: UserSchema
        responses:
            201, 400, 500:
                description: Created, Bad Request, Internal Error
                schema:
                    type: object
                    properties:
                        "message": {"type": "string"}
        """
        json_user = get_json_user()
        user = User(**json_user)
        user.save("Error adding user")
        return {"message": "User added successfully"}, CREATED
