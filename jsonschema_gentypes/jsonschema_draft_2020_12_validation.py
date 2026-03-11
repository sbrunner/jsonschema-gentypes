"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
r""" Validation vocabulary meta-schema. """


class JSONSchemaItemD2020(TypedDict, total=False):
    type: "_ValidationVocabularyMetaSchemaObjectType"
    r""" Aggregation type: anyOf """

    const: Any
    enum: list[Any]
    multipleOf: int | float
    r""" exclusiveMinimum: 0 """

    maximum: int | float
    exclusiveMaximum: int | float
    minimum: int | float
    exclusiveMinimum: int | float
    maxLength: "_NonNegativeInteger"
    r""" minimum: 0 """

    minLength: "_NonNegativeInteger"
    r""" minimum: 0 """

    pattern: str
    r""" format: regex """

    maxItems: "_NonNegativeInteger"
    r""" minimum: 0 """

    minItems: "_NonNegativeInteger"
    r""" minimum: 0 """

    uniqueItems: bool
    r""" default: False """

    maxContains: "_NonNegativeInteger"
    r""" minimum: 0 """

    minContains: "_NonNegativeInteger"
    r""" minimum: 0 """

    maxProperties: "_NonNegativeInteger"
    r""" minimum: 0 """

    minProperties: "_NonNegativeInteger"
    r""" minimum: 0 """

    required: "_StringArray"
    r"""
    uniqueItems: True
    default:
      []
    """

    dependentRequired: dict[str, "_StringArray"]


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
r""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
r""" minimum: 0 """


_STRING_ARRAY_DEFAULT: list[Any] = []
r""" Default value of the field path 'string array' """


_SimpleTypes = Literal["array", "boolean", "integer", "null", "number", "object", "string"]
_SIMPLETYPES_ARRAY: Literal["array"] = "array"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_BOOLEAN: Literal["boolean"] = "boolean"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_INTEGER: Literal["integer"] = "integer"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NULL: Literal["null"] = "null"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NUMBER: Literal["number"] = "number"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_OBJECT: Literal["object"] = "object"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_STRING: Literal["string"] = "string"
r"""The values for the '_SimpleTypes' enum"""


_StringArray = list[str]
r"""
uniqueItems: True
default:
  []
"""


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
r""" Default value of the field path 'Validation vocabulary meta-schema object minContains' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
r""" Default value of the field path 'Validation vocabulary meta-schema object uniqueItems' """


_ValidationVocabularyMetaSchemaObjectType = Union[
    "_SimpleTypes", "_ValidationVocabularyMetaSchemaObjectTypeAnyof1"
]
r""" Aggregation type: anyOf """


_ValidationVocabularyMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
r"""
minItems: 1
uniqueItems: True
"""
