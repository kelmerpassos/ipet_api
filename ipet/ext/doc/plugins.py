"""Automates the resource registration process in apispec."""
from apispec import APISpec
from flask import Flask, current_app


def automatic_mapping(spec: APISpec, app: Flask):
    """Search for OpenAPI configuration docstrings in all View Functions \
    with names ending with 'resource'.

    Args:
        spec (APISpec): APISpec instance.
        app (Flask): Aplication instance.
    """
    if app is None:
        app = current_app
    for view in filter(lambda x: x[0][-8:] == "resource", app.view_functions.items()):
        spec.path(view=view[1], app=app)
