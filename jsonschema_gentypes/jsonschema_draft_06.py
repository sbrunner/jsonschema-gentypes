"""Automatically generated file from a JSON schema."""

from typing import Any, Literal, TypedDict, Union

CORE_SCHEMA_META_SCHEMA_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'JSONSchemaD6' """


JSONSchemaD6 = Union["JSONSchemaItemD6", bool]
"""
Core schema meta-schema.

default:
  {}
"""


# default:
#   {}
JSONSchemaItemD6 = TypedDict(
    "JSONSchemaItemD6",
    {
        # format: uri-reference
        "$id": str,
        # format: uri
        "$schema": str,
        # format: uri-reference
        "$ref": str,
        "title": str,
        "description": str,
        "default": Union[str, Union[int, float], dict[str, Any], list[Any], bool, None],
        "examples": list[Union[str, Union[int, float], dict[str, Any], list[Any], bool, None]],
        # exclusiveMinimum: 0
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        "exclusiveMaximum": Union[int, float],
        "minimum": Union[int, float],
        "exclusiveMinimum": Union[int, float],
        # minimum: 0
        "maxLength": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minLength": "_NonNegativeIntegerDefault0",
        # format: regex
        "pattern": str,
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "additionalItems": "JSONSchemaD6",
        # default:
        #   {}
        #
        # Aggregation type: anyOf
        "items": "_CoreSchemaMetaSchemaObjectItems",
        # minimum: 0
        "maxItems": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minItems": "_NonNegativeIntegerDefault0",
        # default: False
        "uniqueItems": bool,
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "contains": "JSONSchemaD6",
        # minimum: 0
        "maxProperties": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minProperties": "_NonNegativeIntegerDefault0",
        # uniqueItems: True
        # default:
        #   []
        "required": "_StringArray",
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "additionalProperties": "JSONSchemaD6",
        # default:
        #   {}
        "definitions": dict[str, "JSONSchemaD6"],
        # default:
        #   {}
        "properties": dict[str, "JSONSchemaD6"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchemaD6"],
        "dependencies": dict[str, "_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties"],
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "propertyNames": "JSONSchemaD6",
        "const": Union[str, Union[int, float], dict[str, Any], list[Any], bool, None],
        # minItems: 1
        # uniqueItems: True
        "enum": list[Any],
        # Aggregation type: anyOf
        "type": "_CoreSchemaMetaSchemaObjectType",
        "format": str,
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "not": "JSONSchemaD6",
    },
    total=False,
)


_CORE_SCHEMA_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object definitions' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_ITEMS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object items' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object patternProperties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object properties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object uniqueItems' """


_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties = Union["JSONSchemaD6", "_StringArray"]
""" Aggregation type: anyOf """


_CoreSchemaMetaSchemaObjectItems = Union["JSONSchemaD6", "_SchemaArray"]
"""
default:
  {}

Aggregation type: anyOf
"""


_CoreSchemaMetaSchemaObjectType = Union["_SimpleTypes", "_CoreSchemaMetaSchemaObjectTypeAnyof1"]
""" Aggregation type: anyOf """


_CoreSchemaMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_NonNegativeIntegerDefault0 = int
"""
minimum: 0
default: 0
"""


_STRING_ARRAY_DEFAULT: list[Any] = []
""" Default value of the field path 'string array' """


_SchemaArray = list["JSONSchemaD6"]
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
uniqueItems: True
default:
  []
"""
