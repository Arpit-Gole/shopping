"""
A testing suite to test creation and deletion of the database.
"""

import pytest

from shopping.orm.setup import (
    DATABASE_PATH,
    check_if_db_exists,
    close_session,
    create_database,
)


@pytest.fixture
def remove_db():
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
    yield
    close_session()
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()


def test_database_creation_pass(remove_db):
    create_database()
    assert DATABASE_PATH.exists()


def test_database_creation_fail(remove_db):
    # Intentionally failing test by checking the existence of a DB before creation
    with pytest.raises(AssertionError):
        assert check_if_db_exists()
