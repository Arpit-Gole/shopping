"""
A module to setup the database and create the tables.
"""

import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)


# A static DB to simulate the real world DB interactions.
DATABASE_URL = "sqlite:///data_rock_shopping.db"
DATABASE_PATH = Path.cwd().joinpath(DATABASE_URL.replace("sqlite:///", ""))

# A session connection to simulate the real world transaction.
_ENGINE = create_engine(DATABASE_URL, echo=False)
_SESSION = sessionmaker(bind=_ENGINE)()
Base = declarative_base()


def check_if_db_exists():
    return DATABASE_PATH.exists()


def create_database(scratch: bool = False) -> None:
    """
    A helper function to create a db.
    """

    if scratch and DATABASE_PATH.exists():
        log.info("Deleting the existing db.")
        DATABASE_PATH.unlink(missing_ok=True)

    Base.metadata.create_all(bind=_ENGINE)


def create_session() -> sessionmaker:
    """
    A helper function to a current session connection to the db.
    """
    return _SESSION


def close_session() -> None:
    """
    A helper function to close the current session connection to the db.
    """
    _SESSION.close()
    _ENGINE.dispose()
