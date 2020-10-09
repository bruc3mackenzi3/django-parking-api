import calendar
from datetime import datetime
import logging


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
        """

        if cls.rates == None:
            return None

        for rate in cls.rates:
            if rate.time_span_in_rate(start, end):
                return rate.price
        return None

    @classmethod
    def rates_loaded(cls) -> bool:
        return bool(cls.rates)

class Rate:
    def __init__(self, days: str, times: str, timezone: str, price: int):
        self.days = days
        self.times = times
        self.timezone = timezone
        self.price = price

    @property
    def days(self) -> list:   # todo: specify nested type
        return self._days

    @days.setter
    def days(self, value: str) -> None:
        fields = value.lower().split(",")
        for day in fields:
            if day not in day_abbreviations:
                raise ValueError(f"Day is not a valid day abbreviation: {day}")
        self._days = fields

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

        return True
