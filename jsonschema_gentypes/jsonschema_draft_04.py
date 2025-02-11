"""Automatically generated file from a JSON schema."""

from typing import Any, Literal, TypedDict, Union

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
        "default": Union[str, Union[int, float], dict[str, Any], list[Any], bool, None],
        # minimum: 0
        # exclusiveMinimum: True
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        # default: False
        "exclusiveMaximum": bool,
        "minimum": Union[int, float],
        # default: False
        "exclusiveMinimum": bool,
        # minimum: 0
        "maxLength": "_PositiveInteger",
        # minimum: 0
        # default: 0
        "minLength": "_PositiveIntegerDefault0",
        # format: regex
        "pattern": str,
        # default:
        #   {}
        #
        # Aggregation type: anyOf
        "additionalItems": "_Jsonschemad4Additionalitems",
        # default:
        #   {}
        #
        # Aggregation type: anyOf
        "items": "_Jsonschemad4Items",
        # minimum: 0
        "maxItems": "_PositiveInteger",
        # minimum: 0
        # default: 0
        "minItems": "_PositiveIntegerDefault0",
        # default: False
        "uniqueItems": bool,
        # minimum: 0
        "maxProperties": "_PositiveInteger",
        # minimum: 0
        # default: 0
        "minProperties": "_PositiveIntegerDefault0",
        # minItems: 1
        # uniqueItems: True
        "required": "_StringArray",
        # default:
        #   {}
        #
        # Aggregation type: anyOf
        "additionalProperties": "_Jsonschemad4Additionalproperties",
        # default:
        #   {}
        "definitions": dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "properties": dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchemaD4"],
        "dependencies": dict[str, "_Jsonschemad4DependenciesAdditionalproperties"],
        # minItems: 1
        # uniqueItems: True
        "enum": list[Any],
        # Aggregation type: anyOf
        "type": "_Jsonschemad4Type",
        "format": str,
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
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
        "not": "JSONSchemaD4",
    },
    total=False,
)


_JSONSCHEMAD4_ADDITIONALITEMS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 additionalItems' """


_JSONSCHEMAD4_ADDITIONALPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 additionalProperties' """


_JSONSCHEMAD4_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4' """


_JSONSCHEMAD4_DEFINITIONS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 definitions' """


_JSONSCHEMAD4_EXCLUSIVEMAXIMUM_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 exclusiveMaximum' """


_JSONSCHEMAD4_EXCLUSIVEMINIMUM_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 exclusiveMinimum' """


_JSONSCHEMAD4_ITEMS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 items' """


_JSONSCHEMAD4_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 patternProperties' """


_JSONSCHEMAD4_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD4 properties' """


_JSONSCHEMAD4_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'JSONSchemaD4 uniqueItems' """


_Jsonschemad4Additionalitems = Union[bool, "JSONSchemaD4"]
"""
default:
  {}

Aggregation type: anyOf
"""


_Jsonschemad4Additionalproperties = Union[bool, "JSONSchemaD4"]
"""
default:
  {}

Aggregation type: anyOf
"""


_Jsonschemad4DependenciesAdditionalproperties = Union["JSONSchemaD4", "_StringArray"]
""" Aggregation type: anyOf """


_Jsonschemad4Items = Union["JSONSchemaD4", "_SchemaArray"]
"""
default:
  {}

Aggregation type: anyOf
"""


_Jsonschemad4Type = Union["_SimpleTypes", "_Jsonschemad4TypeAnyof1"]
""" Aggregation type: anyOf """


_Jsonschemad4TypeAnyof1 = list["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_POSITIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'positive integer default0' """


_PositiveInteger = int
""" minimum: 0 """


_PositiveIntegerDefault0 = int
"""
minimum: 0
default: 0
"""


_SchemaArray = list["JSONSchemaD4"]
""" minItems: 1 """


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
minItems: 1
uniqueItems: True
"""
