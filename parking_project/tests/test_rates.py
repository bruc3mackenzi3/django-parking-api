import pytest

from parking_app.lib.rates import TimeSpan


rates_file_path = 'tests/data/rates.json'


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
