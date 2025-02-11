"""Automatically generated file from a JSON schema."""

from typing import Any, Literal, TypedDict, Union

CORE_SCHEMA_META_SCHEMA_DEFAULT = True
""" Default value of the field path 'JSONSchemaD7' """


JSONSchemaD7 = Union["JSONSchemaItemD7", bool]
"""
Core schema meta-schema.

default: True
"""


# default: True
JSONSchemaItemD7 = TypedDict(
    "JSONSchemaItemD7",
    {
        # format: uri-reference
        "$id": str,
        # format: uri
        "$schema": str,
        # format: uri-reference
        "$ref": str,
        "$comment": str,
        "title": str,
        "description": str,
        "default": Any,
        # default: False
        "readOnly": bool,
        # default: False
        "writeOnly": bool,
        "examples": list[Any],
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
        # default: True
        "additionalItems": "JSONSchemaD7",
        # default: True
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
        # default: True
        "contains": "JSONSchemaD7",
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
        # default: True
        "additionalProperties": "JSONSchemaD7",
        # default:
        #   {}
        "definitions": dict[str, "JSONSchemaD7"],
        # default:
        #   {}
        "properties": dict[str, "JSONSchemaD7"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchemaD7"],
        "dependencies": dict[str, "_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties"],
        # Core schema meta-schema.
        #
        # default: True
        "propertyNames": "JSONSchemaD7",
        "const": Any,
        # minItems: 1
        # uniqueItems: True
        "enum": list[Any],
        # Aggregation type: anyOf
        "type": "_CoreSchemaMetaSchemaObjectType",
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        # Core schema meta-schema.
        #
        # default: True
        "if": "JSONSchemaD7",
        # Core schema meta-schema.
        #
        # default: True
        "then": "JSONSchemaD7",
        # Core schema meta-schema.
        #
        # default: True
        "else": "JSONSchemaD7",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Core schema meta-schema.
        #
        # default: True
        "not": "JSONSchemaD7",
    },
    total=False,
)


_CORE_SCHEMA_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object definitions' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_ITEMS_DEFAULT = True
""" Default value of the field path 'Core schema meta-schema object items' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object patternProperties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object properties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object readOnly' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object uniqueItems' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object writeOnly' """


_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties = Union["JSONSchemaD7", "_StringArray"]
""" Aggregation type: anyOf """


_CoreSchemaMetaSchemaObjectItems = Union["JSONSchemaD7", "_SchemaArray"]
"""
default: True

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


_SchemaArray = list["JSONSchemaD7"]
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
