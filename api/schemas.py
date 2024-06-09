"""This is the schemas file

Contains all schemas for crud operations.
"""

from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    """This is the base schema for the Address model"""
    address: str
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)

class AddressCreate(AddressBase):
    """This is the create schema for the Address model"""

class AddressReturn(AddressBase):
    """This is the return schema for the Address model"""
    address_id: int

    class Config:
        """To allow orm mode"""
        orm_mode = True
