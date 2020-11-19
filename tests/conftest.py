import pytest
import responses


@pytest.fixture
def mocked_response():
    """A pytest fixture to mock the behaviour of a server sending back a response."""
    with responses.RequestsMock() as mocked_response:
        yield mocked_response


@pytest.fixture
def mocked_successful_post_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
                "nbCreated": 0,
                "nbUpdated": 6,
                "nbFailed": 0,
                "nbDeactivated": 0,
                "created": [],
                "updated": [
                    '207', '673', '676', '680', '684', '748'
                ],
                "failed": [],
                "deactivated": []
        },
        status=200,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 10:06:41 GMT',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
            },
    )


@pytest.fixture
def mocked_400_status_code_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
            'type': '/errors/BadRequestError',
            'status': 400,
            'title': 'Input CSV file is improperly formatted',
        },
        status=400,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 15:10:34 GMT',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )


@pytest.fixture
def mocked_500_status_code_request(mocked_response):
    mocked_response.add(
        responses.POST,
        url="https://watchlistapi.icedatavault.icedataservices.com/v1/configurations/watchlists",
        json={
            "type": "/errors/NoSuchElementException",
            "status": 500,
        },
        status=500,
        content_type="application/json;charset=UTF-8",
        headers={
            'Date': 'Wed, 18 Nov 2020 15:23:52 GMT',
            'Content-Type': 'application/json;charset=UTF-8',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'x-request-with, authorization, content-type',
            'Access-Control-Allow-Credentials': 'true',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains',
            'X-Frame-Options': 'DENY'
        },
    )
