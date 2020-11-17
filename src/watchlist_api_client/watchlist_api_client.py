"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import csv
import pathlib
import re
from typing import Tuple

import requests

from watchlist_api_client.data_structures import ConfigSummary


class InvalidHeaderFormat(Exception):
    pass


class InvalidConfigFileFormat(Exception):
    pass


def check_existence_of_config_file(path_to_config_file: str) -> bool:
    return pathlib.Path(path_to_config_file).is_file()


def validate_header(header: str) -> str:
    header_pattern = r"^sourceId,RTSsymbol$"
    if not re.match(header_pattern, header):
        raise InvalidHeaderFormat(
            f"The header of the file does not conform the prescribed format. Expected "
            f"'sourceId,RTSsymbol', got '{header}'.",
        )
    return header


def validate_row(row: str, row_index: int) -> str:
    row_pattern = r"^[0-9]{{3,4}},[A-Z1-9\\+;(!-*.:/)$@&_%#]+$"
    if not re.match(row_pattern, row):
        raise InvalidConfigFileFormat(
            f"Line {row_index} improperly formatted.",
        )
    return row


def validate_watchlist_configuration_file(path_to_watchlist_config_file: str) -> str:
    with pathlib.Path(path_to_watchlist_config_file).open('r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(csv_reader):
            if index == 0:
                validate_header(','.join(row))
            else:
                validate_row(','.join(row), index)
    return path_to_watchlist_config_file


def send_config(
    watchlist_endpoint: str, credentials: Tuple[str, str], path_to_watchlist_config_file: str,
) -> ConfigSummary:
    request_payload = {"file": pathlib.Path(path_to_watchlist_config_file).open('rb')}
    with requests.post(watchlist_endpoint, auth=credentials, files=request_payload) as response:
        if response.status_code == 200:
            return ConfigSummary(
                submission_time=response.headers.get('Date'),
                summary=response.json(),
            )
        elif response.status_code == 400:
            raise ConnectionError(
                f"The request failed with status code: {response.status_code}\n"
                f"Error: ImproperCSVFormat\n"
                f"Error description: input CSV file is improperly formatted.",
            )
        elif response.status_code == 401:
            raise ConnectionError(
                f"The request failed with status code: {response.status_code}\n"
                f"Error: {response.json().get('error').capitalize()}\n"
                f"Error description: {response.json().get('error_description').lower()}.",
            )
        elif response.status_code == 500:
            raise ConnectionError(
                f"The request failed with status code: {response.status_code}\n"
                f"Error: UnsuccessfulRequest\n"
                f"Error description: the request as a whole failed.",
            )
        else:
            raise ConnectionError(f"The request failed with status code: {response.status_code}")
