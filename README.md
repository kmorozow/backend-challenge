# Westcott Multimedia - Backend Developer Challenge

## Task

Imagine a simple Flask app with a database managed by SQLAlchemy and the models/tables described in `app/models/models.py`.

Please write an API endpoint as a new /metrics route defined in `app/__init__.py` that accepts a GET request with a "metric_value" parameter and returns all days when any existing artist 'crossed' that metric value, i.e. when the artist's metric_value on that day is larger than or equal to and its value on the previous day is lower than the passed parameter value.

Such function needs to
- Fetch all metrics
- Find the days when any artist crossed the passed value
- Return a list of all artists as dictionaries with the artist id and all "crossings" = day(s) the metric crossed the specified value, e.g. [{"artist_id": 1, "crossings": ["2020-01-01"]}, {"artist_id": 2, "crossings": []}]

If everything works as expected, the respective unit test defined in `tests/tests.py` should pass.

## Setup

1. Create virtual environment and install dependencies with the Poetry package manager
(see more information about Poetry at https://github.com/python-poetry/poetry)
```shell
$ poetry install
```

2. Test app locally without database
(serve from one and access from another terminal window)
```shell
$ poetry run flask run
Serving Flask app...
```
```shell
$ curl http://127.0.0.1:5000/ping
Server is here
```

3. Run tests
```shell
$ poetry run coverage run -m unittest
```
