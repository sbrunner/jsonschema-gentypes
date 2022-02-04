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
    lineLength: int
    generate: List["GenerateItem"]


# Generate item
class GenerateItem(TypedDict, total=False):
    source: str
    destination: str
    root_name: str
    api_arguments: "ApiArguments"
    name_mapping: Dict[str, str]
