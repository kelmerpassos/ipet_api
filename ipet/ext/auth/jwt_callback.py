"""JTW callback module."""
from typing import Union

from flask_jwt_extended import JWTManager

from ipet.ext.auth.models import User
from ipet.ext.db import db_redis


def register_callbacks(jwt: JWTManager):
    """Register custom jwt callbacks.

    Args:
        jwt (JWTManager): JWTManager instance.
    """

    @jwt.user_identity_loader
    def user_identity_lookup(identity: Union[User, int]):
        """Use to convert an identity to a JSON serializable \
        format when creating JWTs. This is useful for using objects (such as \
        SQLAlchemy instances) as the identity when creating your tokens.

        Args:
            identity (Union[User, int]): Identity that was used when creating a JWT.

        Returns:
            Return the Identity.
        """
        if type(identity) is User:
            return identity.id
        return identity

    @jwt.user_lookup_loader
    def user_loockup_callback(_, jwt_playload):
        """Use to convert a JWT into a python object that can \
        be used in a protected endpoint. This is useful for automatically \
        loading a SQLAlchemy instance based on the contents of the JWT.

        Args:
            _ (dict): Dictionary containing the header data of the JWT.
            jwt_playload (dict): Dictionary containing the payload data of the JWT.

        Returns:
            (User): Return a user instance.
        """
        identity = jwt_playload["sub"]
        return User.query.get(identity)

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(_, jwt_playload):
        """Use to check if a JWT has been revoked.

        Args:
            _ (dict): Dictionary containing the header data of the JWT.
            jwt_playload (dict): Dictionary containing the payload data of the JWT.

        Returns:
            The function must be return ``True`` if the token has been
            revoked, ``False`` otherwise.
        """
        jti = jwt_playload["jti"]
        token_in_redis = db_redis.get(jti)
        return token_in_redis is not None
