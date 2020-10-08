# django-parking-api

## Build Instructions
This project is built using Pipenv.  Install Pipenv with the following command:

```
pip install pipenv
```

Build project with the command:

```
pipenv sync --dev
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
Note: This creates nested folders, both named `parking_project`

Setup project Database (run from _outer_ parking_project/ folder):
```
python manage.py migrate
```

Create Django app (run from _outer_ parking_project/ folder):
```
python manage.py startapp parking_app
```

## Testing
```
curl "http://127.0.0.1:8000/parking_rates?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00"
```
