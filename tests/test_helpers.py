import pytest
import datetime
import dateutil.tz

from watchlist_api_client import helpers


class TestParseUTCTimestamp:
    @pytest.mark.parametrize(
        "raw_utc_timestamp, expected_timestamp", [
            (
                'Wed, 18 Nov 2020 15:23:52 GMT',
                datetime.datetime(2020, 11, 18, 15, 23, 52, tzinfo=dateutil.tz.tzutc())
             ),
            (
                "2020-11-18T15:23:52Z",
                datetime.datetime(2020, 11, 18, 15, 23, 52, tzinfo=dateutil.tz.tzutc()),
             )
        ]
    )
    def test_parsing_of_raw_timestamp(self, raw_utc_timestamp, expected_timestamp):
        # Setup - none
        # Exercise
        parsed_timestamp = helpers.parse_utc_timestamp(raw_utc_timestamp)
        # Verify
        assert parsed_timestamp == expected_timestamp
        # Cleanup - none


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
