"""
Automatically generated file from a JSON schema.
"""


from typing import Dict, List, Literal, TypedDict, Union

AdditionalProperties = Union[Literal["Always"], Literal["Only explicit"]]
"""
Additional properties.

Describe how to deal with additional properties
"""
ADDITIONALPROPERTIES_ALWAYS: Literal["Always"] = "Always"
"""The values for the 'Additional properties' enum"""
ADDITIONALPROPERTIES_ONLY_EXPLICIT: Literal["Only explicit"] = "Only explicit"
"""The values for the 'Additional properties' enum"""


class ApiArguments(TypedDict, total=False):
    """
    API arguments.

    The argument passed to the API
    """

    additional_properties: "AdditionalProperties"


class Configuration(TypedDict, total=False):
    """
    Configuration.

    The JSON Schema generate Python types configuration
    """

    headers: str
    callbacks: List[List[str]]
    lineLength: int
    """The maximum line length"""

    generate: List["GenerateItem"]
    """required"""


class GenerateItem(TypedDict, total=False):
    """Generate item."""

    source: str
    """
    The JSON schema file name

    required
    """

    destination: str
    """
    The generated Python file name

    required
    """

    root_name: str
    """The name of the root element"""

    api_arguments: "ApiArguments"
    """
    WARNING: The required are not correctly taken in account,
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/6
    """

    name_mapping: Dict[str, str]
    """
    Name mapping.

    Used to map the name of an alternate name
    """
