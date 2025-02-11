"""Automatically generated file from a JSON schema."""

from typing import Any, Literal, TypedDict, Union

JSONSchemaD2019 = Union["JSONSchemaItemD2019", bool]
""" Validation vocabulary meta-schema. """


class JSONSchemaItemD2019(TypedDict, total=False):
    multipleOf: Union[int, float]
    """ exclusiveMinimum: 0 """

    maximum: Union[int, float]
    exclusiveMaximum: Union[int, float]
    minimum: Union[int, float]
    exclusiveMinimum: Union[int, float]
    maxLength: "_NonNegativeInteger"
    """ minimum: 0 """

    minLength: "_NonNegativeInteger"
    """ minimum: 0 """

    pattern: str
    """ format: regex """

    maxItems: "_NonNegativeInteger"
    """ minimum: 0 """

    minItems: "_NonNegativeInteger"
    """ minimum: 0 """

    uniqueItems: bool
    """ default: False """

    maxContains: "_NonNegativeInteger"
    """ minimum: 0 """

    minContains: "_NonNegativeInteger"
    """ minimum: 0 """

    maxProperties: "_NonNegativeInteger"
    """ minimum: 0 """

    minProperties: "_NonNegativeInteger"
    """ minimum: 0 """

    required: "_StringArray"
    """
    uniqueItems: True
    default:
      []
    """

    dependentRequired: dict[str, "_StringArray"]
    const: Any
    enum: list[Any]
    type: "_ValidationVocabularyMetaSchemaObjectType"
    """ Aggregation type: anyOf """


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_STRING_ARRAY_DEFAULT: list[Any] = []
""" Default value of the field path 'string array' """


_SimpleTypes = Literal["array", "boolean", "integer", "null", "number", "object", "string"]
_SIMPLETYPES_ARRAY: Literal["array"] = "array"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_BOOLEAN: Literal["boolean"] = "boolean"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_INTEGER: Literal["integer"] = "integer"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NULL: Literal["null"] = "null"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NUMBER: Literal["number"] = "number"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_OBJECT: Literal["object"] = "object"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_STRING: Literal["string"] = "string"
"""The values for the '_SimpleTypes' enum"""


_StringArray = list[str]
"""
uniqueItems: True
default:
  []
"""


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
""" Default value of the field path 'Validation vocabulary meta-schema object minContains' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Validation vocabulary meta-schema object uniqueItems' """


_ValidationVocabularyMetaSchemaObjectType = Union[
    "_SimpleTypes",
    "_ValidationVocabularyMetaSchemaObjectTypeAnyof1",
]
""" Aggregation type: anyOf """


_ValidationVocabularyMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""
