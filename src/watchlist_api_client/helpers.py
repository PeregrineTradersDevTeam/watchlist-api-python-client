import datetime

import dateutil.parser
import dateutil.tz


def parse_response_timestamp(timestamp: str) -> datetime.datetime:
    return dateutil.parser.parse(timestamp).replace(tzinfo=dateutil.tz.tzutc())


def format_utc_timestamp(
    utc_timestamp: datetime.datetime,
    date_format: str = "%Y-%m-%dT%H:%M:%SZ",
) -> str:
    return datetime.datetime.strftime(utc_timestamp, date_format)


def convert_raw_utc_timestamp_to_string(
    raw_timestamp: str,
    date_format: str = "%Y-%m-%dT%H:%M:%SZ",
) -> str:
    return format_utc_timestamp(parse_response_timestamp(raw_timestamp), date_format)
