"""
Module containing the command line app.
"""
import pathlib
import sys
from typing import Tuple

import click
import requests

from watchlist_api_client import config_retriever, config_sender, helpers


class MissingOnyxCredentialsError(Exception):
    """A class for an exception to raise in case of missing credentials."""


def validate_credentials(credentials: Tuple[str, str]) -> None:
    username, password = credentials
    if all(credential is None for credential in credentials):
        raise MissingOnyxCredentialsError('Missing username and password')
    elif any(credential is None for credential in credentials):
        if username is None:
            raise MissingOnyxCredentialsError('Missing username')
        else:
            raise MissingOnyxCredentialsError('Missing password')


@click.group()
def watchlist():
    pass


@watchlist.command(name="submit")
@click.argument('config_file', type=click.Path(exists=True))
@click.option('-u', '--user', type=str, envvar="ICE_API_USERNAME")
@click.option('-p', '--password', type=str, envvar="ICE_API_PASSWORD")
@click.option('-q', '--quiet', is_flag=True)
@click.option('-l', '--log-output', is_flag=True)
@click.option('-w', '--write-to', type=click.Path(exists=True),
              default=pathlib.Path().cwd().as_posix())
def send_config(config_file, user, password, quiet, log_output, write_to):
    try:
        config_sender.validate_watchlist_configuration_file(config_file)
    except config_sender.ImproperFileFormat as e:
        click.echo(f"Invalid Configuration File: {str(e)}")
        sys.exit(1)

    credentials = (user, password)
    try:
        validate_credentials(credentials)
    except MissingOnyxCredentialsError as missing_credentials_error:
        click.echo(f"Missing Credentials Error: {str(missing_credentials_error)}")

    watchlist_api_endpoint = (
        "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
    )
    known_error_causes = {
        "400": "Input CSV file is improperly formatted",
        "401": "Improper credentials",
        "500": "Failed request"
    }
    try:
        config_summary = config_sender.send_config(
            watchlist_api_endpoint,
            credentials,
            path_to_watchlist_config_file=config_file
        )
    except requests.exceptions.HTTPError as http_error:
        error_type = str(http_error).split(":")[0]
        error_code = error_type[:3]
        if error_code in known_error_causes.keys():
            click.echo(f"{error_type}: {known_error_causes.get(error_code)}")
        else:
            click.echo(f"{error_type}")
        sys.exit(1)

    if not quiet:
        click.echo(config_sender.stringify_response_summary(config_summary))

    if log_output:
        path_to_request_summary = config_sender.write_request_summary_to_json(
            config_summary, write_to
        )
        click.echo(
            f"The summary of the actions performed as a result of the request has been written to: "
            f"\n"
            f"  {path_to_request_summary}"
        )


@watchlist.command(name="retrieve")
@click.option('-u', '--user', type=str, envvar="ICE_API_USERNAME")
@click.option('-p', '--password', type=str, envvar="ICE_API_PASSWORD")
@click.option('-t', '--timestamp', type=str, default=None)
@click.option('-w', '--write-to', type=click.Path(exists=True),
              default=pathlib.Path().cwd().as_posix())
def get_config(user, password, timestamp, write_to):
    credentials = (user, password)
    try:
        validate_credentials(credentials)
    except MissingOnyxCredentialsError as missing_credentials_error:
        click.echo(f"Missing Credentials Error: {str(missing_credentials_error)}")

    watchlist_api_endpoint = (
        "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
    )
    if timestamp:
        watchlist_api_endpoint = helpers.join_base_url_and_query_string(
            watchlist_api_endpoint,
            helpers.prepare_timestamp_query_string(
                helpers.convert_raw_utc_timestamp_to_string(timestamp)
            )
        )

    known_error_causes = {
        "404": "No active configuration for the given date and time",
    }
    try:
        retrieved_configuration = config_retriever.retrieve_config(
            watchlist_api_endpoint,
            credentials
        )
        file_path = config_retriever.retrieved_config_writer(retrieved_configuration, write_to)
        click.echo(
            f"The retrieved_configuration has been written to: "
            f"\n"
            f"  {file_path}"
        )
    except requests.exceptions.HTTPError as http_error:
        error_type = str(http_error).split(":")[0]
        error_code = error_type[:3]
        if error_code in known_error_causes.keys():
            click.echo(f"{error_type}: {known_error_causes.get(error_code)}")
        else:
            click.echo(f"{error_type}")
        sys.exit(1)


if __name__ == '__main__':
    watchlist()
