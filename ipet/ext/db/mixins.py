"""Auxiliary module for writing in database."""
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import InternalServerError


class ManagementMixin:
    """Class to be inherited by models, for saving and deleting elements."""

    @staticmethod
    def __get_db() -> SQLAlchemy:
        """Return to SQLAlchemy instance.

        Returns:
            SQLAlchemy: SQLAlchemy instance.
        """
        return current_app.extensions["sqlalchemy"].db

    @classmethod
    def delete(cls, element, error_msg: str = None):
        """Delete an element from the database.

        Args:
            element: Element to be deleted.
            error_msg (str, optional): Error message to be reported. Defaults to None.

        Raises:
            InternalServerError: There was an error in the deletion process.
        """
        db = cls.__get_db()
        try:
            db.session.delete(element)
            db.session.commit()
        except Exception as exp:
            current_app.logger.exception("Error deleting element")
            db.session.rollback()
            raise InternalServerError(error_msg or "Internal Error")

    @classmethod
    def save_element(cls, element, error_msg: str = None):
        """Save an element in the database.

        Args:
            element: Element to be saved.
            error_msg (str, optional): Error message to be reported. Defaults to None.

        Raises:
            InternalServerError: There was an error in the save process.

        Returns:
            Return the saved and updated element.
        """
        db = cls.__get_db()
        try:
            db.session.add(element)
            db.session.commit()
            return element
        except Exception as exp:
            current_app.logger.exception("Error saving element")
            db.session.rollback()
            raise InternalServerError(error_msg or "Internal Error")

    def save(self, error_msg: str = None):
        """Save the instance itself.

        Args:
            error_msg (str, optional): Error message to be reported. Defaults to None.

        Returns:
            Return the saved and updated instance.
        """
        return self.save_element(self, error_msg)
