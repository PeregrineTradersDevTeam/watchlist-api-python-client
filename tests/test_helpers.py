import pytest

from watchlist_api_client import helpers


class TestPrepareTimestampQueryString:
    def test_preparation_of_query_string(self):
        # Setup
        iso_formatted_timestamp = "2020-11-20T16:09:40Z"
        # Exercise
        generated_query_string = helpers.prepare_timestamp_query_string(
            iso_formatted_timestamp
        )
        # Verify
        expected_query_string = "dateTime=2020-11-20T16:09:40Z"
        assert generated_query_string == expected_query_string
        # Cleanup - none


class TestJoinBaseUrlAndQueryString:
    def test_joining_of_combined_url_with_no_slash(self):
        # Setup
        base_url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        query_string = "dateTime=2020-11-20T16:09:40Z"
        # Exercise
        generated_url = helpers.join_base_url_and_query_string(base_url, query_string)
        # Verify
        expected_url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-20T16:09:40Z"
        )
        assert generated_url == expected_url
        # Cleanup - none

    def test_joining_of_combined_url_with_slash(self):
        # Setup
        base_url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists/"
        )
        query_string = "dateTime=2020-11-20T16:09:40Z"
        # Exercise
        generated_url = helpers.join_base_url_and_query_string(base_url, query_string)
        # Verify
        expected_url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-20T16:09:40Z"
        )
        assert generated_url == expected_url
        # Cleanup - none