"""Module that implements serialization and validation of data referring to the authentication's domain."""
from marshmallow import ValidationError, validates

from ipet.ext.auth.models import User
from ipet.ext.libs import ma


class UserSchema(ma.SQLAlchemySchema):
    """User data schema."""

    class Meta:
        """Configure class metadata."""

        model = User

    username = ma.auto_field(description="Username")
    password = ma.auto_field(description="Password")

    @validates("username")
    def unique(self, value):
        """Ensure that there is no duplication of username."""
        if (
            self.context.get("custom_validate")
            and User.query.filter(User.username == value).first()
        ):
            raise ValidationError("Username already exists")


class AuthorizationSchema(ma.Schema):
    """Data schema for header with token."""

    auth = ma.String(description="Token (Bearer)", data_key="Authorization")


class RefreshAuthSchema(ma.Schema):
    """Data schema for header with refresh token."""

    auth = ma.String(description="Refresh Token (Bearer)", data_key="Authorization")


class SimpleTokenSchema(ma.Schema):
    """Data schema that only serializes the token."""

    token = ma.String()


class RefreshTokenSchema(SimpleTokenSchema):
    """Data schema that serializes token and refresh token."""

    refresh_token = ma.String()
