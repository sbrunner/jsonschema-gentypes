from typing import cast

import pytest
from jsonschema import ValidationError

from jsonschema_gentypes.cli import validate_config
from jsonschema_gentypes.configuration import Configuration


def test_validate_config() -> None:
    config_valid: Configuration = Configuration(
        generate=[
            {
                "source": "tests/get_name_properties.json",
                "destination": "tests/get_name_properties.py",
            }
        ],
    )

    validate_config(config_valid)

    config_bad = cast(dict, Configuration(config_valid))
    config_bad["extra parameter"] = "bad parameter"
    with pytest.raises(ValidationError) as validation_error:
        validate_config(config_bad)
    assert validation_error.value.message.startswith("Validation Errors when validating configuration")
    assert (
        "Additional properties are not allowed ('extra parameter' was unexpected)"
        in validation_error.value.message
    )

    config_bad = cast(dict, Configuration(config_valid))
    del config_bad["generate"][0]["source"]
    with pytest.raises(ValidationError) as validation_error:
        validate_config(config_bad)
    assert validation_error.value.message.startswith("Validation Errors when validating configuration")
    assert "'source' is a required property" in validation_error.value.message
