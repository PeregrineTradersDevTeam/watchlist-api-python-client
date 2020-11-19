"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import pathlib
from typing import Tuple

import requests

from watchlist_api_client.data_structures import RequestSummary


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
        summary=response.json()
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
