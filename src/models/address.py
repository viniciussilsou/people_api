from sqlalchemy import Column, Integer, String

from models.base import Base


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {"schema": "people-api"}

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    # street_type = Column(String, nullable=True)
    country = Column(String, nullable=False)
    # estate = Column(String, nullable=True)
    # city = Column(String, nullable=True)
    # neighborhood = Column(String, nullable=True)
    # street = Column(String, nullable=True)
    # number = Column(String, nullable=True)
    # complement = Column(String, nullable=True)
    # postal_code = Column(String, nullable=True)

