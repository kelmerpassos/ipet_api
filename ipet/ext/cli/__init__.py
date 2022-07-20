"""Terminal custom commands registration module."""

import click
from flask import Flask

from ipet.ext.cli import views


def init_app(app: Flask):
    """Register commands.

    Args:
        app (Flask): Aplication instance.
    """

    @app.cli.command()
    def create_db():
        click.echo(views.create_db())

    @app.cli.command()
    def populate_db():
        click.echo(views.populate_db())
