"""
Automatically generated file from a JSON schema.
"""


from enum import Enum
from typing import Dict, List, TypedDict


class AdditionalProperties(Enum):
    """
    Additional properties.

    Describe how to deal with additional properties
    """

    ALWAYS = "Always"
    ONLY_EXPLICIT = "Only explicit"


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
