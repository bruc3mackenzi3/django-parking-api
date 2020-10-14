from datetime import datetime
import pytest

from parking_app.lib.rates import Rate, TimeSpan


rates_file_path = 'tests/data/rates.json'


class TestRate:
    @pytest.mark.parametrize('days, time_span, timezone, price', [
        ('mon', '0900-2100', 'America/Chicago', 1500),
        ('mon,tues', '0900-2100', 'America/Chicago', 1500)
    ])
    def test_init(self, days, time_span, timezone, price):
        rate = Rate(days, time_span, timezone, price)
        assert rate.days == days.split(',')
        assert rate.time_span.start.strftime(TimeSpan.format) == time_span.split('-')[0]
        assert rate.time_span.end.strftime(TimeSpan.format) == time_span.split('-')[1]
        assert str(rate.timezone) == timezone
        assert rate.price == price

    @pytest.mark.parametrize('days, time_span, timezone, price', [
        ('monday', '0900-2100', 'America/Chicago', 1500),  # day
        ('mon', '5555-2100', 'America/Chicago', 1500),  # time
        ('mon', '0900-2100', 'America/Scranton', 1500),    # timezone
        ('mon', '0900-2100', 'America/Chicago', -100),  # price
    ])
    def test_init_invalid(self, days, time_span, timezone, price):
        with pytest.raises(ValueError):
            Rate(days, time_span, timezone, price)

    def test_time_span_in_rate(self):
        rate = Rate('mon', '0900-2100', 'America/Chicago', 1500)
        start = datetime.fromisoformat('2020-10-12T12:00:00-04:00')
        end = datetime.fromisoformat('2020-10-12T18:00:00-04:00')
        assert True == rate.time_span_in_rate(start, end)

        assert False == rate.time_span_in_rate(start, end.replace(hour=23))


class TestTimeSpan:
    @pytest.mark.parametrize('start,end', [
        ('1000', '1200'),
        ('0900', '1200')
    ])
    def test_init(self, start, end):
        span = TimeSpan(f'{start}-{end}')
        assert span.start.strftime(TimeSpan.format) == start
        assert span.end.strftime(TimeSpan.format) == end

    @pytest.mark.parametrize('bad_time_span', [
        '999-1400',    # invalid start time
        '1000-999',    # invalid end time
        '1000-2500',   # invalid hour
        '1000-1261',   # invalid minute
        '1000-0900',   # end time precedes start
        '1000-end',    # bad time value
        '10:00-12:00', # incorrect format
        '1000-1100-1200',
        '-1100-1200'
    ])
    def test_init_invalid(self, bad_time_span):
        with pytest.raises(ValueError):
            TimeSpan(bad_time_span)
