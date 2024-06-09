
# Address API

This is a simple API for a database that stores addresses and coordinates. This project makes use of Python's FastAPI for the framework and SQLite for the database.
## Features

The SQLite database this API connects to has one table named "addresses" which has the following columns: 

    - address_id: int
    - address: str
    - longitude: float
    - latitude: float

This API has the following routes:

    - [GET] /address/{address_id}
        - returns the address given the address_id
    - [POST] /address/
        - adds an address
    - [PUT] /address/
        - updates an address
    - [POST] /get_addresses_by_distance/
        - returns addresses nearest to the provided coordinates with the given distance value
## Environment Variables

To run this project, add the following to the .env file

    DB_NAME="addresses_db"

## Run Locally

Clone the project:

```bash
  git clone https://github.com/cezarate/Address-API.git
```

Go to the project directory:

```bash
  cd Address-API
```

Install dependencies:

```bash
  poetry shell
  poetry install
```

Run:
```bash
  uvicorn api.main:app --reload
```
## 🚀 About Me
I'm a software developer.

