""" This is the crud file

It contains necessary crud operations for the API
"""
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from api import models, schemas
from api import logger


def get_address(db: Session, address_id: int):
    """ Gets the address with the given address_id
    
    Keyword Arguments:
    db -- The database session
    address_id -- The id of the address

    Returns the address if it exists. Returns None otherwise
    Raises MultipleResultsFound if there is more than one record.
    """
    try:
        address = db.query(models.Address).filter(
            models.Address.address_id == address_id).one_or_none()
        if address:
            return address
        raise NoResultFound(address_id)
    except MultipleResultsFound as e:
        logger.exception(
            "Violated duplicate key constraint, check database table for constraints: %s", e)
        raise
    except NoResultFound as e:
        logger.exception(
            "No result found for the given record: %s", e)
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while getting the address: %s", e)
        raise


def add_address(db: Session, address: schemas.AddressCreate):
    """ Adds the provided address to the database
    
    Keyword Arguments:
    db -- The database session
    address -- The given address (model)

    Returns the added address if it does not yet exist in the database.
    Raises IntegrityError otherwise.
    """

    try:
        address_to_add = models.Address(
            address=address.address,
            longitude=address.longitude,
            latitude=address.latitude
        )
        db.add(address_to_add)
        db.commit()
        return address_to_add
    except IntegrityError as e:
        logger.exception("Duplicate key constraint: %s", e)
        db.rollback()
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while adding the address: %s", e)
        raise


def update_address(db: Session, address: schemas.AddressReturn):
    """ Updates the provided address
    
    Keyword Arguments:
    db -- The database session
    address -- The given address (model)

    Updates and returns the address if it exists in the database.
    Raises NoResultFound otherwise.
    Raises MultipleResultsDFound if multiple records are returned.
    """

    try:
        existing_address = db.query(models.Address).filter(
            models.Address.address_id == address.address_id).one_or_none()
        if existing_address:
            existing_address.address = address.address
            existing_address.longitude = address.longitude
            existing_address.latitude = address.latitude

            db.commit()
            return existing_address
        else:
            logger.exception("No results found for given address.")
            raise NoResultFound(address.address_id)
    except MultipleResultsFound as e:
        logger.exception(
            "Violated duplicate key constraint, check database table for constraints: %s", e)
        raise
    except NoResultFound as e:
        logger.exception(
            "No result found for the given record: %s", e)
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while updating the address: %s", e)
        raise


def get_addresses_by_distance(db: Session, longitude: float, latitude: float, distance: float):
    """ Gets all addresses near to the provided coordinates with respect to the given distance
    using the Haversine formula.
    
    Keyword Arguments:
    db -- The database session
    longitude -- the longitude of the provided coordinate
    latitude -- the latitude of the provided coordinate
    distance -- provided distance to find nearby addresses (in km)

    Updates and returns the address if it exists in the database.
    Raises NoResultFound otherwise.
    Raises MultipleResultsDFound if multiple records are returned.
    """

    try:
        filter_stmt = """acos(sin(radians(latitude))*sin(radians(:latitude))+
            cos(radians(latitude))*cos(radians(:latitude))*
            cos(radians(:longitude)-radians(longitude)))*6371 <= :d"""
        addresses = db.query(models.Address).filter(text(filter_stmt)).params(
            longitude=longitude, latitude=latitude, d=distance).all()
        return addresses
    except Exception as e:
        logger.exception(
            "Something went wrong while getting addresses by distance: %s", e)
        raise
