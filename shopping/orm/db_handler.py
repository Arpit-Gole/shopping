"""
A wrapper class to interact with the database.
An interface for the CRUD operations.
"""

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from shopping.orm.setup import create_session
from shopping.utilities.exceptions import DbError


class DbHandler:
    def __init__(self, session: Session = None) -> None:
        if session is None:
            self.session = create_session()
        else:
            self.session = session

    def create(self, obj: object) -> object:
        try:
            self.session.add(obj)
            self.session.commit()
            return obj
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DbError("Failed to create record") from ex

    def read_all(self, model: object) -> list[object]:
        try:
            return self.session.query(model).all()
        except SQLAlchemyError as ex:
            raise DbError("Failed to read record") from ex

    def read_by_id(self, model: object, record_id: int) -> object:
        try:
            return self.session.query(model).get(record_id)
        except SQLAlchemyError as ex:
            raise DbError("Failed to read record with ID %s", record_id) from ex

    def read_by_filter(self, model: object, filters: dict) -> list[object]:
        """
        Read rows from the database where column values match the given filters.
        """
        try:
            query = self.session.query(model)
            conditions = [getattr(model, key) == value for key, value in filters.items()]
            return query.filter(and_(*conditions)).all()
        except SQLAlchemyError as ex:
            raise DbError("Failed to read records with given filters") from ex

    def update(self, obj: object) -> object:
        try:
            self.session.merge(obj)
            self.session.commit()
            return obj
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DbError("Failed to update record") from ex

    def delete(self, obj: object) -> None:
        try:
            self.session.delete(obj)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DbError("Failed to delete record") from ex
