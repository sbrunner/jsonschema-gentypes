from typing import Optional, Union

from jsonschema_gentypes import jsonschema_draft_04, jsonschema_draft_2019_09_meta_data, normalize
from jsonschema_gentypes.cli import process_config
from jsonschema_gentypes.configuration import Configuration


def custom_get_name(
    schema: Optional[
        Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
        ]
    ],
    proposed_name: Optional[str] = None,
    upper: bool = False,
) -> str:
    """
    Custom get the name for an element.

    Just capitalize first Letter, don't do `.title`

    Parameter:
        schema: the concerned schema
        proposed_name: a name that we will use it the schema hasn't any title
        upper: should we use an upper case (For constants)
    """
    # Get the base name
    has_title = isinstance(schema, dict) and "title" in schema
    name = schema["title"] if has_title else proposed_name  # type: ignore
    assert name is not None
    name = normalize(name)

    prefix = "" if has_title else "_"
    if upper:
        # Upper case
        name = name.upper()
        # Remove spaces
        return prefix + "".join(["_" if char.isspace() else char for char in name])
    else:
        # Title case
        name = name[0].upper() + name[1:]
        # Remove spaces
        return prefix + "".join([char for char in name if not char.isspace()])


def test_empty_array() -> None:
    config: Configuration = Configuration(
        generate=[
            {
                "source": "tests/custom_get_name.json",
                "destination": "tests/custom_get_name.py",
                "api_arguments": {"custom_get_name": custom_get_name},
            }
        ],
    )
    process_config(
        config,
        ["tests/custom_get_name.json"],
    )

    with open("tests/custom_get_name.py") as f:
        content = f.read()
        assert "class SubresourceUris" in content
