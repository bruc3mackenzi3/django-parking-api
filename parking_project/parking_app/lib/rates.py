import calendar
from datetime import datetime, time
import logging

import pytz


logger = logging.getLogger(__name__)
day_abbreviations = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]


class ParkingRates:
    rates = None

    @classmethod
    def load_rates(cls, new_rates: dict) -> None:
        """
        Update rates to the new parking rates.

        Args:
            new_rates: New parking rates to update with
        """

        loaded_rates = []
        for rate in new_rates["rates"]:
            loaded_rates.append(Rate(rate["days"], rate["times"], rate["tz"], rate["price"]))

        cls.rates = loaded_rates
        logger.info("Updated parking rates")

    @classmethod
    def get_rate_price(cls, start: datetime, end: datetime) -> int:
        """
        Get the parking rate for supplied start and end times.

        Args:
            start: The start of the time range
            end: The end of the time range

        Returns:
            The applicable rate, None if a rate is not available for the given
            time range.

        Raises:
            RuntimeError if get_rate_price is called before rates are
            successfully loaded.
        """

        if cls.rates == None:
            raise RuntimeError("Rates must first be loaded with load_rates")

        for rate in cls.rates:
            if rate.time_span_in_rate(start, end):
                return rate.price
        return None

    @classmethod
    def rates_loaded(cls) -> bool:
        return bool(cls.rates)


class Rate:
    """
    Class Representing a rate object.

    Args:
        days: Weekdays rate applies to.  Specified with format "mon,wed,fri".
        times: Start and end times rate applies to.  Specified with format
            "0800-1200".
        timezone: Timezone rate applies to.  Specified in format "America/Chicago".
        price: Price for this rate during specified times, specified in cents,
            e.g. 925.

    Raises:
        ValueError if any fields contain invalid data
    """

    def __init__(self, days: str, times: str, timezone: str, price: int):
        self.days = days

        self.time_span = TimeSpan(times)

        try:
            self.timezone = pytz.timezone(timezone)
        except Exception as e:
            raise ValueError from e

        self.price = price

    @property
    def days(self) -> list[str]:
        return self._days

    @days.setter
    def days(self, value: str) -> None:
        fields = value.lower().split(",")
        for day in fields:
            if day not in day_abbreviations:
                raise ValueError(f"Day is not a valid day abbreviation: {day}")
        self._days = fields

    @property
    def price(self) -> str:
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        if type(value) != int or value < 0:
            raise ValueError(f'Invalid price {value}, must be a positive integer')
        self._price = value

    def time_span_in_rate(self, start: datetime, end: datetime) -> bool:
        """
        Returns true if the day and start and end times are within this rate,
        false otherwise.

        Args:
            start: The start of the time range
            end: The end of the time range

        Returns:
            Bool indicating whether time span is within this rate.
        """

        # Convert times to timezone of this Rate
        start_local = start.astimezone(self.timezone)
        end_local = end.astimezone(self.timezone)

        # Ensure times are on same day
        # Note: This can only be checked after timezone conversion is done
        day = start_local.weekday()
        if day != end_local.weekday():
            return False

        # Check day
        if not day_abbreviations[day] in self.days:
            return False

        # Check time
        if not self.time_span.in_time_span(start_local.time(), end_local.time()):
            return False

        return True


class TimeSpan:
    """
    Class representing a time span, i.e. start and end times.

    Args:
        span: Time span represented with format: "0900-2100"

    Raises:
        ValueError if span is not a valid time span.
    """

    format = "%H%M"

    def __init__(self, span: str):
        self.start, self.end = span.split("-")
        if self.start >= self.end:
            raise ValueError(f"Start time {self.start} does not suceed end time {self.end}")

    @property
    def start(self) -> time:
        return self._start

    @start.setter
    def start(self, value: str) -> None:
        self._start = self._parse_time(value)  # Todo: test invalid time

    @property
    def end(self) -> time:
        return self._end

    @end.setter
    def end(self, value: str) -> None:
        self._end = self._parse_time(value)

    def _parse_time(self, value: str) -> time:
        return datetime.strptime(value, self.format).time()

    def in_time_span(self, start: time, end: time) -> bool:
        """
        Check if start and end time objects are inside the time span.

        Args:
            start: The start of the time range
            end: The end of the time range

        Returns: True if both start and end time fall in the time span,
            False otherwise.
        """

        return self.start <= start and self.end >= end
