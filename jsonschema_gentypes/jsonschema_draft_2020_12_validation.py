"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
""" Validation vocabulary meta-schema. """


class JSONSchemaItemD2020(TypedDict, total=False):
    type: Union["_SimpleTypes", "_ValidationVocabularyMetaSchemaObjectTypeAnyof1"]
    const: Any
    enum: List[Any]
    multipleOf: Union[int, float]
    """ exclusiveMinimum: 0 """

    maximum: Union[int, float]
    exclusiveMaximum: Union[int, float]
    minimum: Union[int, float]
    exclusiveMinimum: Union[int, float]
    maxLength: "_NonNegativeInteger"
    minLength: "_NonNegativeInteger"
    pattern: str
    """ format: regex """

    maxItems: "_NonNegativeInteger"
    minItems: "_NonNegativeInteger"
    uniqueItems: bool
    """ default: False """

    maxContains: "_NonNegativeInteger"
    minContains: "_NonNegativeInteger"
    maxProperties: "_NonNegativeInteger"
    minProperties: "_NonNegativeInteger"
    required: "_StringArray"
    dependentRequired: Dict[str, "_StringArray"]


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_STRING_ARRAY_DEFAULT: List[Any] = []
""" Default value of the field path 'string array' """


_SimpleTypes = Union[
    Literal["array"],
    Literal["boolean"],
    Literal["integer"],
    Literal["null"],
    Literal["number"],
    Literal["object"],
    Literal["string"],
]
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


_StringArray = List[str]
"""
uniqueItems: True
default:
  []
"""


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
""" Default value of the field path 'Validation vocabulary meta-schema object minContains' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINLENGTH_DEFAULT = 0
""" Default value of the field path 'Validation vocabulary meta-schema object minLength' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_REQUIRED_DEFAULT: List[Any] = []
""" Default value of the field path 'Validation vocabulary meta-schema object required' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Validation vocabulary meta-schema object uniqueItems' """


_ValidationVocabularyMetaSchemaObjectTypeAnyof1 = List["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""
