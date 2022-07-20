"""Settings packege initialization module."""
from dynaconf import FlaskDynaconf
from flask import Flask

from ipet.ext.config.environment import EnvironmentVar

environment_var = EnvironmentVar()


def init_app(app: Flask):
    """Initialize module in application. \
    The dynaconf library manages the initialization of packages and configuration variables.

    Args:
        app (Flask): Aplication instance.
    """
    FlaskDynaconf(app, extensions_list="INSTALLED_EXTENSIONS")
    environment_var.init_app(app)
