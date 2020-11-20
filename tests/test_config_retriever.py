import pytest
import requests

from watchlist_api_client import config_retriever


class TestInferTimestampFromRetrievedResponse:
    def test_inference_of_timestamp_from_url_without_query_string(
        self,
        mocked_active_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
        )
        # Exercise
        with requests.get(url) as response:
            inferred_timestamp = config_retriever.infer_timestamp_from_retrieved_response(
                response,
            )
        # Verify
        expected_timestamp = "20201120T114740Z"
        assert inferred_timestamp == expected_timestamp
        # Cleanup - none

    def test_inference_of_timestamp_from_url_with_query_string(
        self,
        mocked_deactivated_configuration_response
    ):
        # Setup
        url = (
            "https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists"
            "?dateTime=2020-11-18T12:30:52Z"
        )
        # Exercise
        with requests.get(url) as response:
            inferred_timestamp = config_retriever.infer_timestamp_from_retrieved_response(
                response,
            )
        # Verify
        expected_timestamp = "20201118T123052Z"
        assert inferred_timestamp == expected_timestamp
        # Cleanup - none
