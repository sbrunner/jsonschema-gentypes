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
class ApiArguments(TypedDict, total=False):
    additional_properties: "AdditionalProperties"


# Configuration
#
# The JSON Schema generate Python types configuration
class Configuration(TypedDict, total=False):
    headers: str
    callbacks: List[List[str]]
    # The maximum line length
    lineLength: int
    # required
    generate: List["GenerateItem"]


# Generate item
class GenerateItem(TypedDict, total=False):
    # The JSON schema file name
    #
    # required
    source: str
    # The generated Python file name
    #
    # required
    destination: str
    # The name of the root element
    root_name: str
    # WARNING: The required are not correctly taken in account,
    # See: https://github.com/camptocamp/jsonschema-gentypes/issues/6
    api_arguments: "ApiArguments"
    # Name mapping
    #
    # Used to map the name of an alternate name
    name_mapping: Dict[str, str]
