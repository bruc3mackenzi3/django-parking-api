from datetime import datetime
import json


def validate_get_parking(start: str, end: str) -> tuple[datetime, datetime]:
    """
    Validates the input parameters and returns the parsed result.

    Args:
        start: Start time as a datetime string
        end: End time as a datetime string

    Returns:
        A 2-tuple containing start and end datetime objects

    Raises:
        ValueError if start or end is not a valid datetime string in ISO-8061
        format or does not include timezone info.
    """

    start_datetime = datetime.fromisoformat(start)
    end_datetime = datetime.fromisoformat(end)

    if None in (start_datetime.tzinfo, end_datetime.tzinfo):
        raise ValueError("Timezone must be specified.")

    if start_datetime >= end_datetime:
        raise ValueError(f"Start time does not precede end time.")

    return (start_datetime, end_datetime)


def validate_put_parking(body: str) -> dict:
    """
    Validates the parking rates string passed from the client is a) valid JSON
    and b) a valid rates object.

    NOTE: This function is incomplete

    Args:
        body: The request body which, if valid, contains a JSON string
            representing the rates object

    Returns:
        The rates object as a dictionary.

    Raises:
        ValueError if the passed string is invalid
    """

    try:
        rates = json.loads(body)
    except json.JSONDecodeError as e:
        raise ValueError from e
    else:
        return rates
