"""
Module containing the command line app.
"""
import sys
from typing import Tuple

import click
import requests

from watchlist_api_client import config_sender


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


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('-u', '--user', type=str, envvar="ICE_API_USERNAME")
@click.option('-p', '--password', type=str, envvar="ICE_API_PASSWORD")
def sendconfig(config_file, user, password):
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
    click.echo(config_sender.stringify_response_summary(config_summary))
    # TODO: include the steps to visualize the config summary


if __name__ == '__main__':
    sendconfig()
