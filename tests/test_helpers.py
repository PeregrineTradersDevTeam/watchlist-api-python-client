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
