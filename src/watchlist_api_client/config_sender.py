"""Implements the utilities needed to validate and submit a configuration file to the Watchlist API.

"""
import csv
import pathlib
import re
from typing import Tuple

import requests

from watchlist_api_client.data_structures import RequestSummary


class ImproperFileFormat(Exception):
    """An exception class that is raised when a Watchlist config file is improperly formatted"""
    pass


def validate_header(header: str) -> None:
    """Validates if the header of a Watchlist config file is properly formatted.

    Parameters
    ----------
    header: str
        The header of a Watchlist configuration file.

    Raises
    ------
    ImproperFileFormat
        The exception is accompanied by a message that informs that the header is not
        formatted accordingly to the specification.
    """
    header_pattern = r"^sourceId,RTSsymbol$"
    if not re.match(header_pattern, header):
        raise ImproperFileFormat("Improperly formatted header")


def validate_row(row: str, row_index: int) -> None:
    """Validates if a Watchlist configuration file's row is properly formatted.

    Using a regular expression, the function checks if the components in the passed row
    are in the correct order (first the source ID, followed by a comma, and the instrument
    symbol) and if the symbol is specified in a valid format (containing only the allowed
    characters for the definition of instruments symbols within the ICE Consolidated Feed
    data platform).

    Parameters
    ----------
    row: str
        A row of a Watchlist configuration file.
    row_index: str
        The index of the row passed as an input to the function.

    Raises
    ------
    ImproperFileFormat
        The exception is accompanied by a message informing that a row is not formatted
        accordingly to the specifications, together with the index of the row within the
        file.
    """
    row_pattern = r"^[0-9]{3,4},[A-Z0-9\\+;()!*\-.:/$@&_%#]+$"
    if not re.match(row_pattern, row):
        raise ImproperFileFormat(f"Line {row_index} - Improperly formatted")


def validate_watchlist_configuration_file(path_to_watchlist_config_file: str) -> None:
    """Checks if a Watchlist configuration file is properly formatted.

    Parameters
    ----------
    path_to_watchlist_config_file: str
        The location of the Watchlist configuration file to validate.

    Raises
    ------
    ImproperFileFormat
        If the passed file is not properly formatted, an ImproperFileFormat exception is
        raised, with attached a message that informs whether the file has an invalid
        formatting due to a mis-formatted header or due to a mis-formatted row.
    """
    with pathlib.Path(path_to_watchlist_config_file).open('r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(csv_reader):
            if index == 0:
                validate_header(','.join(row))
            else:
                validate_row(','.join(row), index)


def react_to_status_code_200(response: requests.Response) -> RequestSummary:
    """Embeds the submission time and the subscription summary in a ConfigSummary object.

    The function is designed to deal with the scenario of a successful request to update
    the configuration of the personal profile on the Watchlist API. In case of a
    successful submission of a new configuration file, in fact, the Watchlist API returns
    a JSON object that contains the summary of the actions performed as a result of the
    update request, stating the sources that were created, updated, duplicated, unchanged,
    failed and missing.

    The request summary, together with the timestamp of the response, are stored in a
    RequestSummary named-tuple and returned for further use.

    Parameters
    ----------
    response: requests.Response
        A Response object obtained by submitting a POST request to the Watchlist API.

    Returns
    -------
    RequestSummary
        A RequestSummary named-tuple containing the timestamp of the response and a
        dictionary that contains the summary of the action performed as a result of
        the request to update the configuration of the watchlist configuration file.
    """
    return RequestSummary(
        submission_time=response.headers.get('Date'),
        summary=response.json(),
    )


def send_config(
    watchlist_endpoint: str,
    credentials: Tuple[str, str],
    path_to_watchlist_config_file: str,
) -> RequestSummary:
    """Submits a Watchlist configuration file and returns the request summary.

    The function sends a POST request to the Watchlist API POST endpoint, with the new
    configuration file as a payload of the request. Depending on whether the request is
    successful or not, it returns a RequestSummary named-tuple containing the timestamp
    of the response and the request summary, or raises an HTTPError with the status code
    associated with the failed request.

    Parameters
    ----------
    watchlist_endpoint: str
        The POST endpoint of the Watchlist API.
    credentials: Tuple[str, str]
        A tuple containing the user name and password used to access the Watchlist API.
    path_to_watchlist_config_file
        The path to the location of the Watchlist configuration file that has to be
        uploaded.

    Returns
    -------
    RequestSummary
        A RequestSummary named-tuple containing the timestamp of the response and a
        dictionary that contains the summary of the action performed as a result of
        the request to update the configuration of the watchlist configuration file.

    Raises
    ------
    requests.exceptions.HTTPError
        In case the API call is not successful, returns an HTTPError with the status code
        and the type of error that occurred (whether the error was initiated on the client
        side or on the server side).

    """
    config_payload = {"file": pathlib.Path(path_to_watchlist_config_file).read_bytes()}
    with requests.post(watchlist_endpoint, auth=credentials, files=config_payload) as response:
        response.raise_for_status()
        return react_to_status_code_200(response)
