from jsonschema_gentypes.cli import process_config
from jsonschema_gentypes.configuration import Configuration


def test_empty_array() -> None:
    config: Configuration = Configuration(
        generate=[
            {
                "source": "tests/get_name_properties.json",
                "destination": "tests/get_name_properties.py",
                "api_arguments": {"get_name_properties": "UpperFirst"},
            }
        ],
    )
    process_config(
        config,
        ["tests/get_name_properties.json"],
    )

    with open("tests/get_name_properties.py") as f:
        content = f.read()
        assert "class SubresourceUris" in content
