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

from watchlist_api_client.data_structures import ConfigSummary


def react_to_status_code_200(response: requests.Response) -> ConfigSummary:
    return ConfigSummary(
        submission_time=response.headers.get('Date'),
        summary=response.json()
    )


def send_config(
    watchlist_endpoint: str,
    credentials: Tuple[str, str],
    path_to_watchlist_config_file: str,
) -> ConfigSummary:
    config_payload = {"file": pathlib.Path(path_to_watchlist_config_file).open('rb')}
    with requests.post(watchlist_endpoint, auth=credentials, files=config_payload) as response:
        response.raise_for_status()
        return react_to_status_code_200(response)
