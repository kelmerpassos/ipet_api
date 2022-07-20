"""Module that registers OpenAPI routes."""
from apispec import APISpec
from flask import Blueprint, render_template


def register_routes(bp: Blueprint, spec: APISpec):
    """Register packet routes.

    Args:
        bp (Blueprint): Package blueprint instance.
        spec (APISpec): _description_
    """

    @bp.get("/ui.json")
    def swagger_spec_json():
        return spec.to_dict()

    @bp.get("/ui")
    def swagger_spec_ui():
        return render_template("swagger.html")
