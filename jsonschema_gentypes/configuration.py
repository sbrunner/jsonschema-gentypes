"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict

from typing_extensions import Required

AdditionalProperties = Literal["Always", "Only explicit"]
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
    """
    Additional properties.

    Describe how to deal with additional properties
    """

    get_name_properties: "GetNameProperties"
    """
    Get name properties.

    Describe the rules to use to get the name of an element
    """


class Configuration(TypedDict, total=False):
    """
    Configuration.

    The JSON Schema generate Python types configuration
    """

    headers: str
    callbacks: list[list[str]]
    pre_commit: "PreCommitConfiguration"
    """
    Pre-commit configuration.

    The pre-commit configuration
    """

    lineLength: int
    """ The maximum line length """

    python_version: str
    """ The minimum Python version to support. """

    generate: Required[list["GenerateItem"]]
    """ Required property """


class GenerateItem(TypedDict, total=False):
    """Generate item."""

    source: Required[str]
    """
    The JSON schema file name

    Required property
    """

    destination: Required[str]
    """
    The generated Python file name

    Required property
    """

    root_name: str
    """ The name of the root element """

    api_arguments: "ApiArguments"
    """
    API arguments.

    The argument passed to the API
    """

    name_mapping: dict[str, str]
    """
    Name mapping.

    Used to map the name of an alternate name
    """

    vocabularies: dict[str, str]
    """
    vocabularies.

    Used to add some vocabularies
    """

    local_resources: list[str]
    """ Locally available resources. """


GetNameProperties = Literal["Title", "UpperFirst"]
"""
Get name properties.

Describe the rules to use to get the name of an element
"""
GETNAMEPROPERTIES_TITLE: Literal["Title"] = "Title"
"""The values for the 'Get name properties' enum"""
GETNAMEPROPERTIES_UPPERFIRST: Literal["UpperFirst"] = "UpperFirst"
"""The values for the 'Get name properties' enum"""


PRE_COMMIT_ARGUMENTS_DEFAULT: list[Any] = []
""" Default value of the field path 'Pre-commit configuration arguments' """


PRE_COMMIT_ENABLE_DEFAULT = False
""" Default value of the field path 'Pre-commit configuration enable' """


class PreCommitConfiguration(TypedDict, total=False):
    """
    Pre-commit configuration.

    The pre-commit configuration
    """

    enable: bool
    """
    Pre-commit enable.

    default: False
    """

    arguments: list[str]
    """
    Pre-commit arguments.

    Additional pre-commit arguments

    default:
      []
    """

    hooks: list[str]
    """
    Pre-commit hooks.

    The hooks to run, all by default
    """

    hooks_skip: list[str]
    """
    Pre-commit skipped hooks.

    The hooks to skip, none by default
    """
