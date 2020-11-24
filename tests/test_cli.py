import pytest

from watchlist_api_client.scripts import cli


class TestValidateCredentialsType:
    def test_validation_of_type_with_correct_credentials_tuple(self):
        # Setup
        credentials = ("Username", "Password")
        # Exercise
        # Verify
        assert cli.validate_credentials_type(credentials) is None
        # Cleanup - none

    def test_validation_of_type_with_tuple_with_one_wrong_credential(self):
        # Setup
        credentials = (12345, "Password")
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials_type(credentials)
        # Cleanup - none

    def test_validation_of_type_with_tuple_with_both_credentials_wrong(self):
        # Setup
        credentials = (12345, 6789)
        # Exercise
        # Verify
        with pytest.raises(cli.InvalidOnyxCredentialTypeError):
            cli.validate_credentials_type(credentials)
        # Cleanup - none

