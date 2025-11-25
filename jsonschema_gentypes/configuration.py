"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict

from typing_extensions import Required

AdditionalProperties = Literal["Always", "Only explicit"]
r"""
Additional properties.

Describe how to deal with additional properties
"""
ADDITIONALPROPERTIES_ALWAYS: Literal["Always"] = "Always"
r"""The values for the 'Additional properties' enum"""
ADDITIONALPROPERTIES_ONLY_EXPLICIT: Literal["Only explicit"] = "Only explicit"
r"""The values for the 'Additional properties' enum"""


class ApiArguments(TypedDict, total=False):
    r"""
    API arguments.

    The argument passed to the API
    """

    additional_properties: "AdditionalProperties"
    r"""
    Additional properties.

    Describe how to deal with additional properties
    """

    get_name_properties: "GetNameProperties"
    r"""
    Get name properties.

    Describe the rules to use to get the name of an element
    """


class Configuration(TypedDict, total=False):
    r"""
    Configuration.

    The JSON Schema generate Python types configuration
    """

    headers: str
    callbacks: list[list[str]]
    pre_commit: "PreCommitConfiguration"
    r"""
    Pre-commit configuration.

    The pre-commit configuration
    """

    lineLength: int
    r""" The maximum line length """

    python_version: str
    r""" The minimum Python version to support. """

    generate: Required[list["GenerateItem"]]
    r""" Required property """


class GenerateItem(TypedDict, total=False):
    r"""Generate item."""

    source: Required[str]
    r"""
    The JSON schema file name

    Required property
    """

    destination: Required[str]
    r"""
    The generated Python file name

    Required property
    """

    root_name: str
    r""" The name of the root element """

    api_arguments: "ApiArguments"
    r"""
    API arguments.

    The argument passed to the API
    """

    name_mapping: dict[str, str]
    r"""
    Name mapping.

    Used to map the name of an alternate name
    """

    vocabularies: dict[str, str]
    r"""
    vocabularies.

    Used to add some vocabularies
    """

    local_resources: list[str]
    r""" Locally available resources. """


GetNameProperties = Literal["Title", "UpperFirst"]
r"""
Get name properties.

Describe the rules to use to get the name of an element
"""
GETNAMEPROPERTIES_TITLE: Literal["Title"] = "Title"
r"""The values for the 'Get name properties' enum"""
GETNAMEPROPERTIES_UPPERFIRST: Literal["UpperFirst"] = "UpperFirst"
r"""The values for the 'Get name properties' enum"""


PRE_COMMIT_ARGUMENTS_DEFAULT: list[Any] = []
r""" Default value of the field path 'Pre-commit configuration arguments' """


PRE_COMMIT_ENABLE_DEFAULT = False
r""" Default value of the field path 'Pre-commit configuration enable' """


class PreCommitConfiguration(TypedDict, total=False):
    r"""
    Pre-commit configuration.

    The pre-commit configuration
    """

    enable: bool
    r"""
    Pre-commit enable.

    default: False
    """

    arguments: list[str]
    r"""
    Pre-commit arguments.

    Additional pre-commit arguments

    default:
      []
    """

    hooks: list[str]
    r"""
    Pre-commit hooks.

    The hooks to run, all by default
    """

    hooks_skip: list[str]
    r"""
    Pre-commit skipped hooks.

    The hooks to skip, none by default
    """
