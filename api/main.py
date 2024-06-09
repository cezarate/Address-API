""" This is the main file

It contains the routes and exception handling.
"""
from typing import Annotated
from fastapi import Depends, FastAPI, status, Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from api import crud, models, schemas
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """ Creates and yields the database session. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """ Handles all raised IntegrityErrors.

    Returns error code 400, Duplicate key constraint violated 
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": [{"msg": "Duplicate key constraint violated"}]}),
    )

@app.exception_handler(MultipleResultsFound)
async def multiple_results_exception_handler(request: Request, exc: MultipleResultsFound):
    """ Handles all raised MultipleResultsFound.

    Returns error code 500, Internal Server Error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": [{"msg": "Internal Server Error"}]}),
    )

@app.exception_handler(NoResultFound)
async def no_result_exception_handler(request: Request, exc: NoResultFound):
    """ Handles all raised NoResultFound.

    Returns error code 404, Record not found
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"detail": [{"msg": "Record not found"}]}),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """ Handles unhandled raised exceptions
    
    Returns error code 500, Internal Server Error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": [{"msg": "Internal Server Error"}]}),
    )


@app.get("/address/{address_id}", response_model=schemas.AddressReturn)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    """ A GET request for returning the address given the address_id 
    
    Keyword Arguments:
    address_id -- The address_id of the address to retrieve
    db -- The database session

    Returns the address if successful.
    """
    return crud.get_address(db, address_id=address_id)


@app.post("/address/", response_model=schemas.AddressReturn)
async def add_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """ A POST request for adding an address
    
    Keyword Arguments:
    address -- The address to insert
    db -- The database session

    Returns the added address if successful.
    """
    return crud.add_address(db, address=address)


@app.put("/address/", response_model=schemas.AddressReturn)
async def update_address(address: schemas.AddressReturn, db: Session = Depends(get_db)):
    """ A PUT request to update an address
    
    Keyword Arguments:
    address -- The address to update
    db -- The database session

    Returns the updated address if successful.
    """
    return crud.update_address(db, address=address)


@app.post("/get_addresses_by_distance/", response_model=list[schemas.AddressReturn])
async def get_addresses_by_distance(
    longitude: Annotated[float, Query(ge=-180, le=180)],
    latitude: Annotated[float, Query(ge=-180, le=180)],
    distance: Annotated[float, Query(ge=0)],
    db: Session = Depends(get_db)
    ):
    """ A GET request to retrieve all addresses 
    nearest to the provided coordinates given the distance
    
    Keyword Arguments:
    longitude -- The longitude of the coordinate, must be in [-180, 180]
    latitude -- The latitude of the coordinate, must be in [-90, 90]
    distance -- Provided max distance to find the nearest addresses in km, must be non-negative
    db -- The database session
    """
    return crud.get_addresses_by_distance(
        db, longitude=longitude, latitude=latitude, distance=distance)
