"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

CORE_SCHEMA_META_SCHEMA_DEFAULT: Dict[str, Any] = {}
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
        "default": Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None],
        "examples": List[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]],
        # exclusiveMinimum: 0
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        "exclusiveMaximum": Union[int, float],
        "minimum": Union[int, float],
        "exclusiveMinimum": Union[int, float],
        # minimum: 0
        "maxLength": "_NonNegativeInteger",
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
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
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
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
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
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
        "definitions": Dict[str, "JSONSchemaD6"],
        # default:
        #   {}
        "properties": Dict[str, "JSONSchemaD6"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "JSONSchemaD6"],
        "dependencies": Dict[str, "_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties"],
        # Core schema meta-schema.
        #
        # default:
        #   {}
        "propertyNames": "JSONSchemaD6",
        "const": Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None],
        # minItems: 1
        # uniqueItems: True
        "enum": List[Any],
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


_CORE_SCHEMA_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object definitions' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_ITEMS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object items' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object patternProperties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object properties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_REQUIRED_DEFAULT: List[Any] = []
""" Default value of the field path 'Core schema meta-schema object required' """


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


_CoreSchemaMetaSchemaObjectTypeAnyof1 = List["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_NON_NEGATIVE_INTEGER_DEFAULT0_ALLOF1_DEFAULT = 0
""" Default value of the field path 'non negative integer default0 allof1' """


_NonNegativeInteger = int
""" minimum: 0 """


_NonNegativeIntegerDefault0 = Union["_NonNegativeInteger", "_NonNegativeIntegerDefault0Allof1"]
"""
WARNING: PEP 544 does not support an Intersection type,
so `allOf` is interpreted as a `Union` for now.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/8

Aggregation type: allOf
"""


_NonNegativeIntegerDefault0Allof1 = Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
""" default: 0 """


_STRING_ARRAY_DEFAULT: List[Any] = []
""" Default value of the field path 'string array' """


_SchemaArray = List["JSONSchemaD6"]
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
uniqueItems: True
default:
  []
"""
