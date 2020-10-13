# django-parking-api

## Build Instructions
### Local
This project is built using Pipenv.  Install Pipenv with the following command:

```
pip install pipenv
```

Build project with the command:

```
pipenv sync --dev
```

### Docker
From project root folder:
```
docker build -t parking_api .
```

## Run Instructions
To run the Django web server:
```
python manage.py runserver [port] [--noreload]
```

## Project Setup
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

## Testing
### PUT rates
```bash
# Load from valid rates file
curl -X PUT -H "Content-Type: application/json" -d @parking_app/data/rates.json  "http://127.0.0.1:8000/parking_rates"

# JSON with single rate
curl -X PUT -d '{"rates": [{"days": "wed", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"

# Invalid day
curl -X PUT -d '{"rates": [{"days": "wedn", "times": "0600-1800", "tz": "America/Chicago", "price": 1750}]}'  "http://127.0.0.1:8000/parking_rates"
```

### GET rates
```bash
# 1750 parking rate
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# 2000 parking rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-04T15:00:00%2B00:00&end=2015-07-04T20:00:00%2B00:00"
%2B

# Unavailable parking rate (+ symbol URL escaped)
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-04T07:00:00%2B05:00&end=2015-07-04T20:00:00%2B05:00"

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

# Invalid date
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-99T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"
curl "http://127.0.0.1:8000/parking_rates?start=xxxx-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"

# Date range spanning multiple days
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# start time does not precede end time
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-03T07:00:00-05:00&end=2015-07-02T12:00:00-05:00"

# Outside range by 1 minute
curl "http://127.0.0.1:8000/parking_rates?start=2020-10-10T02:00:00-04:00&end=2020-10-10T06:01:00-04:00"
```
