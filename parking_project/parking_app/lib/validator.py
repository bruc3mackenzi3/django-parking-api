from datetime import datetime
import json


def validate_get_parking(start: str, end: str) -> tuple[datetime, datetime]:
    """
    Validates the input parameters and returns the parsed result.

    Args:
        start: Start time as a datetime string
        end: End time as a datetime string

    Returns:
        A 2-Tuple containing start and end datetime objects

    Raises:
        ValueError if start or end is not a valid datetime string in ISO-8061
        format.
    """

    start_datetime = datetime.fromisoformat(start)
    end_datetime = datetime.fromisoformat(end)

    if start_datetime >= end_datetime:
        raise ValueError(f"start time does not precede end time.")

    if not start_datetime.date() == end_datetime.date():
        raise ValueError(f"Start and end dates do not match: {start_datetime.date()} != {end_datetime.date()}")

    return [start_datetime, end_datetime]


def validate_put_parking(body: str) -> dict:
    """
    """

    rates = json.loads(body)
    return rates
