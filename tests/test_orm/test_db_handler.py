"""
A testing suite to test the CRUD operations.
"""

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from shopping.orm.db_handler import DbHandler
from shopping.orm.setup import (
    DATABASE_PATH,
    check_if_db_exists,
    close_session,
    create_database,
    create_session,
)
from shopping.utilities.exceptions import DbError

# Set up the base for tests
Base = declarative_base()


# Example model for testing
class TestModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


@pytest.fixture(scope="module")
def setup_db():
    # Create the database and tables
    create_database(scratch=True)
    Base.metadata.create_all(bind=create_session().bind)
    yield
    close_session()
    if check_if_db_exists():
        DATABASE_PATH.unlink()


@pytest.fixture
def db_handler(setup_db):
    """
    Return a DbHandler instance.
    """
    return DbHandler(session=create_session())


def test_create(db_handler):
    obj = TestModel(name="Test Name")
    created_obj = db_handler.create(obj)
    assert created_obj.id is not None
    assert created_obj.name == "Test Name"


def test_create_failure(db_handler, mocker):
    mocker.patch.object(db_handler.session, "add")
    with pytest.raises(TypeError):
        db_handler.create()


def test_read_all_failure(db_handler, mocker):
    mocker.patch.object(db_handler.session, "query", side_effect=SQLAlchemyError)
    with pytest.raises(DbError):
        db_handler.read_all(TestModel)


def test_read_by_id(db_handler):
    obj = TestModel(name="Test by ID")
    created_obj = db_handler.create(obj)
    found_obj = db_handler.read_by_id(TestModel, created_obj.id)
    assert found_obj is not None
    assert found_obj.id == created_obj.id
    assert found_obj.name == "Test by ID"


def test_read_by_filter(db_handler):
    db_handler.create(TestModel(name="FilterTest1"))
    db_handler.create(TestModel(name="FilterTest2"))

    filters = {"name": "FilterTest1"}
    records = db_handler.read_by_filter(TestModel, filters)
    assert len(records) == 1
    assert records[0].name == "FilterTest1"


def test_read_by_filter_failure(db_handler, mocker):
    mocker.patch.object(db_handler.session, "query", side_effect=SQLAlchemyError)
    filters = {"name": "NonExistingName"}
    with pytest.raises(DbError):
        db_handler.read_by_filter(TestModel, filters)


def test_update(db_handler):
    obj = TestModel(name="Original Name")
    created_obj = db_handler.create(obj)
    created_obj.name = "Updated Name"

    updated_obj = db_handler.update(created_obj)
    assert updated_obj.name == "Updated Name"


def test_update_failure(db_handler, mocker):
    obj = db_handler.create(TestModel(name="Test Name"))
    obj.name = "Updated Name"
    mocker.patch.object(db_handler.session, "merge", side_effect=SQLAlchemyError)
    with pytest.raises(DbError):
        db_handler.update(obj)


def test_delete(db_handler):
    obj = TestModel(name="To Be Deleted")
    created_obj = db_handler.create(obj)

    db_handler.delete(created_obj)

    found_obj = db_handler.read_by_id(TestModel, created_obj.id)
    assert found_obj is None


def test_delete_failure(db_handler, mocker):
    obj = db_handler.create(TestModel(name="Test Name"))
    mocker.patch.object(db_handler.session, "delete", side_effect=SQLAlchemyError)
    with pytest.raises(DbError):
        db_handler.delete(obj)
