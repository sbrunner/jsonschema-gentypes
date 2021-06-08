"""
Automatically generated file from a JSON schema.
"""


from typing import Dict, List, Literal, TypedDict, Union

# Additional properties
#
# Describe how to deal with additional properties
AdditionalProperties = Union[Literal["Always"], Literal["Only explicit"]]
# The values for the enum
ADDITIONALPROPERTIES_ALWAYS: Literal["Always"] = "Always"
ADDITIONALPROPERTIES_ONLY_EXPLICIT: Literal["Only explicit"] = "Only explicit"


# API arguments
#
# The argument passed to the API
ApiArguments = TypedDict(
    "ApiArguments",
    {
        "additional_properties": "AdditionalProperties",
    },
    total=False,
)


# Configuration
#
# The JSON Schema generate Python types configuration
Configuration = TypedDict(
    "Configuration",
    {
        "headers": str,
        "callbacks": List[List[str]],
        # The maximum line length
        "lineLength": int,
        # required
        "generate": List["GenerateItem"],
    },
    total=False,
)


# Generate item
GenerateItem = TypedDict(
    "GenerateItem",
    {
        # The JSON schema file name
        #
        # required
        "source": str,
        # The generated Python file name
        #
        # required
        "destination": str,
        # The name of the root element
        "root_name": str,
        # WARNING: The required are not correctly taken in account,
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/6
        "api_arguments": "ApiArguments",
        # Name mapping
        #
        # comment: Used to map the name of an aleternate name
        "name_mapping": Dict[str, str],
    },
    total=False,
)
