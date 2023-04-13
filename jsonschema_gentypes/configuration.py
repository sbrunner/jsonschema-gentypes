"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

from typing_extensions import Required

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
    pre_commit: "PreCommitConfiguration"
    lineLength: int
    """ The maximum line length """

    python_version: str
    """ The minimum Python version to support. """

    generate: Required[List["GenerateItem"]]
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
    name_mapping: Dict[str, str]
    """
    Name mapping.

    Used to map the name of an alternate name
    """

    vocabularies: Dict[str, str]
    """
    vocabularies.

    Used to add some vocabularies
    """


PRE_COMMIT_ARGUMENTS_DEFAULT: List[Any] = []
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

    arguments: List[str]
    """
    Pre-commit arguments.

    Additional pre-commit arguments

    default:
      []
    """

    hooks: List[str]
    """
    Pre-commit hooks.

    The hooks to run, all by default
    """

    hooks_skip: List[str]
    """
    Pre-commit skipped hooks.

    The hooks to skip, none by default
    """
