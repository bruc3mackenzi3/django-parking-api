from datetime import datetime
import json

import pytest

from parking_app.lib import validator


rates_file_path = 'tests/data/rates.json'


@pytest.mark.parametrize('start,end', [
    ('2015-07-01T07:00:00-05:00', '2015-07-01T12:00:00-05:00'),  # 5 hour time span
    ('2015-07-01T07:00:00+05:00', '2015-07-01T12:00:00+05:00'),
    ('2015-07-01T07:00:00+02:00', '2015-07-01T12:00:00+03:00'),  # different timezones
    ('2015-07-01T07:00:00-05:00', '2015-07-01T06:00:00-08:00'),
    ('2015-07-01T07:00:00', '2015-07-01T12:00:00'),  # no timezone
    ('2015-07-01T00:00:00-05:00', '2015-07-01T23:59:59-05:00'),  # full 24 hours
    ('2015-07-01T07:00:00-05:00', '2015-07-02T12:00:00-05:00')  # multiple days
])
def test_validate_get_parking(start, end):
    start_dt, end_dt = validator.validate_get_parking(start, end)
    assert start_dt == datetime.fromisoformat(start)
    assert end_dt == datetime.fromisoformat(end)


@pytest.mark.parametrize('start,end', [
    ('2015-13-01T07:00:00-05:00', '2015-07-01T12:00:00-05:00'),  # invalid date
    ('2015-xx-01T07:00:00-05:00', '2015-07-01T12:00:00-05:00'),
    ('2015-07-01T25:00:00-05:00', '2015-07-01T12:00:00-05:00'),  # invalid time
    ('2015-07-01T07:61:00-05:00', '2015-07-01T12:00:00-05:00'),
    ('2015-07-01T12:00:00-05:00', '2015-07-01T07:00:00-05:00'),  # start after end time
    ('2015-07-01T07:00:00-07:00', '2015-07-01T08:00:00-05:00')
])
def test_validate_get_parking_invalid(start, end):
    with pytest.raises(ValueError):
        validator.validate_get_parking(start, end)


def test_validate_put_parking():
    rates_str = open(rates_file_path).read()
    rates_dict = validator.validate_put_parking(rates_str)
    assert json.loads(rates_str) == rates_dict


@pytest.mark.parametrize('bad_json', [
    '',
    'invalid json',
    '{ "rates": [ { "days":'
])
def test_validate_put_parking_invalid(bad_json):
    with pytest.raises(ValueError):
        validator.validate_put_parking(bad_json)
