"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

# Core schema meta-schema
#
# id: http://json-schema.org/draft-04/schema#
# dependencies:
#   exclusiveMaximum:
#   - maximum
#   exclusiveMinimum:
#   - minimum
# default:
#   {}
JSONSchemaD4 = TypedDict(
    "JSONSchemaD4",
    {
        "id": str,
        "$schema": str,
        "title": str,
        "description": str,
        # WARNING: we get an schema without any type
        "default": Any,
        # minimum: 0
        # exclusiveMinimum: True
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        # default: False
        "exclusiveMaximum": bool,
        "minimum": Union[int, float],
        # default: False
        "exclusiveMinimum": bool,
        "maxLength": "_PositiveInteger",
        "minLength": "_PositiveIntegerDefault0",
        # format: regex
        "pattern": str,
        # default:
        #   {}
        "additionalItems": Union[bool, "JSONSchemaD4"],
        # default:
        #   {}
        "items": Union["JSONSchemaD4", "_SchemaArray"],
        "maxItems": "_PositiveInteger",
        "minItems": "_PositiveIntegerDefault0",
        # default: False
        "uniqueItems": bool,
        "maxProperties": "_PositiveInteger",
        "minProperties": "_PositiveIntegerDefault0",
        "required": "_StringArray",
        # default:
        #   {}
        "additionalProperties": Union[bool, "JSONSchemaD4"],
        # default:
        #   {}
        "definitions": Dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "properties": Dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "patternProperties": Dict[str, "JSONSchemaD4"],
        "dependencies": Dict[str, Union["JSONSchemaD4", "_StringArray"]],
        # minItems: 1
        # uniqueItems: True
        #
        # WARNING: we get an array without any items
        "enum": None,
        "type": Union["_SimpleTypes", "_Jsonschemad4TypeAnyof1"],
        "format": str,
        "allOf": "_SchemaArray",
        "anyOf": "_SchemaArray",
        "oneOf": "_SchemaArray",
        "not": "JSONSchemaD4",
    },
    total=False,
)


_JSONSCHEMAD4_ADDITIONALITEMS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 additionalItems' """


_JSONSCHEMAD4_ADDITIONALPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 additionalProperties' """


_JSONSCHEMAD4_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4' """


_JSONSCHEMAD4_DEFINITIONS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 definitions' """


_JSONSCHEMAD4_EXCLUSIVEMAXIMUM_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 exclusiveMaximum' """


_JSONSCHEMAD4_EXCLUSIVEMINIMUM_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 exclusiveMinimum' """


_JSONSCHEMAD4_ITEMS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 items' """


_JSONSCHEMAD4_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 patternProperties' """


_JSONSCHEMAD4_PROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 properties' """


_JSONSCHEMAD4_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 uniqueItems' """


_Jsonschemad4TypeAnyof1 = List["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_POSITIVE_INTEGER_DEFAULT0_ALLOF1_DEFAULT = 0
""" Default value of the field path 'positive integer default0 allof1' """


_PositiveInteger = int
""" minimum: 0 """


_PositiveIntegerDefault0 = Union["_PositiveInteger", "_PositiveIntegerDefault0Allof1"]
"""
WARNING: PEP 544 does not support an Intersection type,
so `allOf` is interpreted as a `Union` for now.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
"""


_PositiveIntegerDefault0Allof1 = int
""" default: 0 """


_SchemaArray = List["JSONSchemaD4"]
""" minItems: 1 """


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
minItems: 1
uniqueItems: True
"""
