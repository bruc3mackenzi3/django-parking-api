# django-parking-api
A Django web server that exposes an API for injesting a parking rates document and processing queries for the parking rate during a given time span.


## Build and Run Locally
Python 3.9 or later is required to run the web server.  If your system doesn't meet this requirement it can be [run with Docker](#Building-and-Running-with-Docker).

This project is built using Pipenv.  Install Pipenv with the following command:
```
pip install pipenv
```

Build project with the command:
```
pipenv sync --dev
```

Alternatively the project can be built with virtualenv and pip:
```
virtualenv env
source env/bin/activate
pip install -r requirements-dev.txt
```

To run the Django web server run this command from `parking_project/` (default port is 8000):
```
[pipenv run] python manage.py runserver [port] [--noreload]
```


## Build and Run with Docker
Run commands from project root folder.

To build the container image:
```
docker build -t parking_api .
```

To run the container:
```
docker run -it -p 8000:8000 parking_api
```


## Accessing the API
Published endpoints are documented in the included OpenAPI / Swagger Specification.  A visual representation can be viewed [here](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/bruc3mackenzi3/django-parking-api/main/swagger.yaml).

To load the example parking rates provided run the following curl command from `parking_project/`:

```bash
curl -X PUT -H "Content-Type: application/json" -d @parking_app/data/rates.json  "http://127.0.0.1:8000/park/rates"
```

The loaded parking rates can be queried with this request:
```bash
curl "http://127.0.0.1:8000/park/query?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"
```

Additional example queries are provided below in the [API Tests](#API-Tests) section.


## Solution Overview
* The parking rates are not automatically loaded on startup.  They are manually loaded by sending to the `/park/rates` endpoint.
* The requirement _should support JSON over HTTP_ has been satisfied to the greatest extent possible.  For consistency all requests and responses use JSON except for the rate query request.  For ease of use (e.g. sending request from a browser) the start and end parameters are passed as query parameters in a GET.
* Note because of the presence of a `+` in some ISO datetimes this character must be escaped in requests (replaced with `%2B`).  Alternatively the entire datetime strings may be escaped.
* Different timezones in a given rate query are supported.  This case is tested in the unit tests.  If this were explicitly not a requirement a simpler approach to deny such queries might be favourable.
* The API is intended to be RESTful.  This includes use of appropriate HTTP methods and status codes.  Note for setting the rates in the server PUT is used (rather than POST) because each action is considered an update to existing data rather creating new data.

### Django
* I identified in the first interview I do not have Django experience.  I've taken this assignment as an opportunity to demonstrate my ability to learn a new framework.
* Django features I've made use of include the `LOGGING` config and disabling CSRF to allow PUT requests in `settings.py`.
* In addition views are implemented with View subclasses and their respective HTTP methods to enforce use of correct methods.
* For simplicity the backend libraries are called directly by `views.py`.  This is done for simplicity and because there is no data model or database.


## Testing

### Unit Tests
Unit tests are implemented for the backend modules `rates.py` and `views.py`.

To run unit tests, execute following command from `parking_project/` directory.  Note dev dependencies must be installed and virtual environment activated.
```
PYTHONPATH=. pytest
```

### API Tests
Manual test cases are provided for testing the API as a whole.  Unlike unit tests these end-user, functional tests execute the entire stack including the Django request handlers and the web server itself.  A variety of cases are provided for both expected and erroroneous behaviour, with the expected result in the comment.

#### Set and Update Parking Rates
```sh
# Load from valid rates file
curl -X PUT -H "Content-Type: application/json" -d @parking_app/data/rates.json  "http://127.0.0.1:8000/park/rates"

# JSON with single rate
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/park/rates"

# Invalid day
curl -X PUT -d '{"rates": [{"days": "wedn", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/park/rates"

# Invalid time
curl -X PUT -d '{"rates": [{"days": "wed", "times": "xxxx-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/park/rates"

# Invalid timezone
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Scranton", "price": 1750}]}'  "http://127.0.0.1:8000/park/rates"

# Invalid price
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Chicago", "price": -1750}]}'  "http://127.0.0.1:8000/park/rates"
```

#### Query Parking Rate Prices
```bash
# 1750 parking rate
curl "http://127.0.0.1:8000/park/query?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# 2000 parking rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/park/query?start=2015-07-04T15:00:00%2B00:00&end=2015-07-04T20:00:00%2B00:00"

# 1500 in Eastern Time
curl "http://127.0.0.1:8000/park/query?start=2020-10-08T12:00:00-04:00&end=2020-10-08T18:00:00-04:00"

# 2000 in Eastern Time
curl "http://127.0.0.1:8000/park/query?start=2020-10-09T12:00:00-04:00&end=2020-10-09T18:00:00-04:00"

# 1750 in Eastern Time
curl "http://127.0.0.1:8000/park/query?start=2020-10-07T12:00:00-04:00&end=2020-10-07T18:00:00-04:00"

# 1000 in Eastern Time
curl "http://127.0.0.1:8000/park/query?start=2020-10-10T02:00:00-04:00&end=2020-10-10T06:00:00-04:00"

# 925 in Eastern Time
curl "http://127.0.0.1:8000/park/query?start=2020-10-11T05:00:00-04:00&end=2020-10-11T07:00:00-04:00"

# Unavailable rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/park/query?start=2015-07-04T07:00:00%2B05:00&end=2015-07-04T20:00:00%2B05:00"

# Unavailable rate - Date range spanning multiple days
curl "http://127.0.0.1:8000/park/query?start=2015-07-01T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# Unavailable rate - Date range spanning multiple rates
curl "http://127.0.0.1:8000/park/query?start=2020-10-07T02:00:00-05:00&end=2020-10-07T18:00:00-05:00"

# Invalid date
curl "http://127.0.0.1:8000/park/query?start=2015-07-99T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"
curl "http://127.0.0.1:8000/park/query?start=xxxx-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# Invalid time
curl "http://127.0.0.1:8000/park/query?start=2015-07-01T25:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# start time does not precede end time
curl "http://127.0.0.1:8000/park/query?start=2015-07-03T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# Outside range by 1 minute
curl "http://127.0.0.1:8000/park/query?start=2020-10-10T02:00:00-04:00&end=2020-10-10T06:01:00-04:00"
```


## Development
### Project Setup
Create Django project (run from project root folder):
```
django-admin startproject parking_project
```
Note: This creates nested folders both named `parking_project`

Setup project Database (run from _outer_ parking_project/ folder):
```
python manage.py migrate
```

Create Django app (run from _outer_ parking_project/ folder):
```
python manage.py startapp parking_app [port] [--noreload]
```

Generate requirements.txt
```
pipenv lock -r > requirements-pipenv.txt
```
