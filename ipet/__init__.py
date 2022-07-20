"""Module that creates the flask object and configures root logging."""
import logging

from flask import Flask, redirect, url_for

from ipet.ext import config

logging.basicConfig(
    filename="record.log",
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(funcName)s - - [%(asctime)s] %(message)s",
)


def create_app():
    """Create a flask object.

    Returns:
        Flask: Flask object created.
    """
    app = Flask(__name__, instance_relative_config=True)
    config.init_app(app)

    @app.get("/")
    def index():
        return redirect(url_for("doc.swagger_spec_ui"))

    return app
