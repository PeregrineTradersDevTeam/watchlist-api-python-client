"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from typing import Dict, NamedTuple


class RequestSummary(NamedTuple):
    """Stores the content of the request summary obtained after submitting a new configuration."""
    submission_time: str
    summary: Dict


class RetrievedConfig(NamedTuple):
    """Stores the content of the configuration retrieved from the Watchlist API."""
    timestamp: str
    config_body: bytes
