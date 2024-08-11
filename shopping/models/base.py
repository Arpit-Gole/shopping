"""
A base class to add all the auditing columns.

P.S. This class will not be directly instantiated.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime

from shopping.orm.setup import Base


class Auditing(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
