""" This is the models file

It contains the models for the database tables for this API.
"""
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
from api.database import Base

class Address(Base):
    """ The model for the Addresses Table
    
    Attributes:

    __tablename__ -- The name of the table
    address_id -- The primary id of the address table
    address -- the name of the address
    longitude -- The longitude value of the address
    latitude -- the latitude value of the address

    longitude and latitude as a pair must be unique.
    """
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    address = Column(String, unique=True)
    longitude = Column(Float)
    latitude = Column(Float)

    UniqueConstraint('longitude', 'latitude', name='coordinates_1')
