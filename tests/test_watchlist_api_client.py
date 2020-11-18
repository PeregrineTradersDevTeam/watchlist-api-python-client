import pytest
import responses

from watchlist_api_client import watchlist_api_client as wac
from watchlist_api_client.watchlist_api_client import InvalidHeaderFormat, InvalidConfigFileFormat


class TestValidateHeader:
    def test_validation_of_incorrectly_formatted_header(self):
        # Setup
        header_to_validate = "SourceID,RTSSymbol"
        # Exercise
        # Verify
        with pytest.raises(InvalidHeaderFormat) as invalid_header_format:
            wac.validate_header(header_to_validate)
        assert str(invalid_header_format.value) == (
            f"The header of the file does not conform the prescribed format. Expected "
            f"'sourceId,RTSsymbol', got '{header_to_validate}'."
        )
        # Cleanup - none

    def test_validation_of_correctly_formatted_header(self):
        # Setup
        header_to_validate = "sourceId,RTSsymbol"
        # Exercise
        returned_header = wac.validate_header(header_to_validate)
        # Verify
        assert returned_header == header_to_validate
        # Cleanup - none


class TestValidateRow:
    def test_validation_of_incorrectly_formatted_row(self):
        # Setup
        row_to_validate = "207, F:FDAX\\Z20"
        # Exercise
        # Verify
        with pytest.raises(InvalidConfigFileFormat) as invalid_config_file_format:
            wac.validate_row(row_to_validate, 1)
        assert str(invalid_config_file_format.value) == (
            f"Line 1 improperly formatted."
        )
        # Cleanup - none

    def test_validation_of_row_with_incorrect_symbol(self):
        # Setup
        row_to_validate = "207, F:FDAX??Z20"
        # Exercise
        # Verify
        with pytest.raises(InvalidConfigFileFormat) as invalid_config_file_format:
            wac.validate_row(row_to_validate, 1)
        assert str(invalid_config_file_format.value) == (
            f"Line 1 improperly formatted."
        )
        # Cleanup - none

    def test_validation_of_correctly_formatted_row(self):
        # Setup
        row_to_validate = "207,F:FDAX\\Z20"
        # Exercise
        returned_row = wac.validate_row(row_to_validate, 1)
        # Verify
        assert returned_row == row_to_validate
        # Cleanup - none

