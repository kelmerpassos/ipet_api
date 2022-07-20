"""Module that intermediates the use of environment variables."""
from flask import Flask


class EnvironmentVar:
    """Class that centralizes environment variables needed throughout the application."""

    @classmethod
    def init_app(cls, app: Flask):
        """Initialize the values of the variables.

        Args:
            app (Flask): Aplication instance.
        """
        cls.JWT_ACCESS_TOKEN_EXPIRES = app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
        cls.SSH_HOST = app.config.get("SSH_HOST")
        cls.SSH_PORT = app.config.get("SSH_PORT")
        cls.SSH_USER = app.config.get("SSH_USER")
        cls.SSH_PASSWORD = app.config.get("SSH_PASSWORD")
        cls.DB_FILE_PATH = app.config.get("DB_FILE_PATH")
