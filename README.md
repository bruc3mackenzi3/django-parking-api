# django-parking-api
A Django web server that exposes an API for injesting a parking rates document and processing queries on parking rates.


## Building and Running Locally
Python 3.9 or later is required to run the web server.  If your system doesn't meet this requirement it can be [run with Docker](#Building-and-Running-with-Docker).

This project is built using Pipenv.  Install Pipenv with the following command:
```
pip install pipenv
```

Build project with the command:
```
pipenv sync --dev
```

To run the Django web server (default port is 8000):
```
python manage.py runserver [port] [--noreload]
```


## Building and Running with Docker
Run commands from project root folder.

To build the container image:
```
docker build -t parking_api .
```

To run the container:
```
docker run -it -p 8000:8000 parking_api
```


## Solution Overview
* Different timezones in the rate query are supported.  This case is tested in the unit tests.  If this were explicitly not a requirement a simpler approach would be to deny such queries.
### Django
* I identified in the first interview I do not have Django experience.  I've taken this opportunity to learn the basics of Django and have used it for the web server framework.
* Django features I've made use of include the `LOGGING` config, disabling CSRF to allow PUT requests in `settings.py`.
* For simplicity the backend libraries are called directly by `views.py`.  This is done for simplicity and because there is no data model or database.


## Testing

### Unit Tests
To run unit tests, execute following command from `parking_project/` directory:
```bash
PYTHONPATH=. pytest
```

### API Tests
Manual test cases are provided for testing the API itself.  A variety of cases are provided for both expected and erroroneous behaviour, with the expected result in the comment.

#### PUT rates
```bash
# Load from valid rates file
curl -X PUT -H "Content-Type: application/json" -d @parking_app/data/rates.json  "http://127.0.0.1:8000/parking_rates"

# JSON with single rate
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"

# Invalid day
curl -X PUT -d '{"rates": [{"days": "wedn", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"

# Invalid time
curl -X PUT -d '{"rates": [{"days": "wed", "times": "xxxx-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"

# Invalid timezone
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Scranton", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"

# Invalid price
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Chicago", "price": -1750}]}'  "http://127.0.0.1:8000/parking_rates"
```

#### GET rates
```bash
# 1750 parking rate
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# 2000 parking rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-04T15:00:00%2B00:00&end=2015-07-04T20:00:00%2B00:00"

# 1500 in Eastern Time
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-08T12:00:00-04:00&end=2020-10-08T18:00:00-04:00"

# 2000 in Eastern Time
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-09T12:00:00-04:00&end=2020-10-09T18:00:00-04:00"

# 1750 in Eastern Time
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-07T12:00:00-04:00&end=2020-10-07T18:00:00-04:00"

# 1000 in Eastern Time
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-10T02:00:00-04:00&end=2020-10-10T06:00:00-04:00"

# 925 in Eastern Time
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-11T05:00:00-04:00&end=2020-10-11T07:00:00-04:00"

# Unavailable parking rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-04T07:00:00%2B05:00&end=2015-07-04T20:00:00%2B05:00"

# Invalid date
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-99T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"
curl "http://127.0.0.1:8000/parking_rates?start=xxxx-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# Invalid time
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T25:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# Date range spanning multiple days
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# start time does not precede end time
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-03T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# Outside range by 1 minute
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-10T02:00:00-04:00&end=2020-10-10T06:01:00-04:00"
```


## Developing
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
