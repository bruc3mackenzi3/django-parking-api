from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class ParkingRates:

    rates = None

    @classmethod
    def load_rates(cls, new_rates: dict) -> None:
        """
        Update rates to the new parking rates.

        Args:
            new_rates: New parking rates to update with
        """
        cls.rates = new_rates
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

        if cls.rates != None:
            return cls.rates["rates"][0]['price']
        else:
            return None
