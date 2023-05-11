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
        "default": Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None],
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
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
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
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
        "minItems": "_PositiveIntegerDefault0",
        # default: False
        "uniqueItems": bool,
        # minimum: 0
        "maxProperties": "_PositiveInteger",
        # WARNING: PEP 544 does not support an Intersection type,
        # so `allOf` is interpreted as a `Union` for now.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
        #
        # Aggregation type: allOf
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
        "definitions": Dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "properties": Dict[str, "JSONSchemaD4"],
        # default:
        #   {}
        "patternProperties": Dict[str, "JSONSchemaD4"],
        "dependencies": Dict[str, "_Jsonschemad4DependenciesAdditionalproperties"],
        # minItems: 1
        # uniqueItems: True
        "enum": List[Any],
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

Aggregation type: allOf
"""


_PositiveIntegerDefault0Allof1 = Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
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
