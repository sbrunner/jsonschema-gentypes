"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

CORE_SCHEMA_META_SCHEMA_DEFAULT = True
"""Default value of the field path 'JSONSchema'"""


JSONSchema = Union["JSONSchemaItem", bool]
"""
Core schema meta-schema.

default: True
"""


# default: True
JSONSchemaItem = TypedDict(
    "JSONSchemaItem",
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
        "examples": List[Any],
        # exclusiveMinimum: 0
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        "exclusiveMaximum": Union[int, float],
        "minimum": Union[int, float],
        "exclusiveMinimum": Union[int, float],
        "maxLength": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minLength": "_CoreSchemaMetaSchemaObjectMinlength",
        # format: regex
        "pattern": str,
        "additionalItems": "CoreSchemaMetaSchema",
        # default: True
        "items": Union["CoreSchemaMetaSchema", "_CoreSchemaMetaSchemaObjectItemsAnyof1"],
        "maxItems": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minItems": "_CoreSchemaMetaSchemaObjectMinlength",
        # default: False
        "uniqueItems": bool,
        "contains": "CoreSchemaMetaSchema",
        "maxProperties": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minProperties": "_CoreSchemaMetaSchemaObjectMinlength",
        "required": "_CoreSchemaMetaSchemaObjectRequired",
        "additionalProperties": "CoreSchemaMetaSchema",
        # default:
        #   {}
        "definitions": Dict[str, "CoreSchemaMetaSchema"],
        # default:
        #   {}
        "properties": Dict[str, "CoreSchemaMetaSchema"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "CoreSchemaMetaSchema"],
        "dependencies": Dict[str, Union["CoreSchemaMetaSchema", "_CoreSchemaMetaSchemaObjectRequired"]],
        "propertyNames": "CoreSchemaMetaSchema",
        "const": Any,
        # minItems: 1
        # uniqueItems: True
        "enum": List[Any],
        "type": Union["_CoreSchemaMetaSchemaObjectTypeAnyof0", "_CoreSchemaMetaSchemaObjectTypeAnyof1"],
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        "if": "CoreSchemaMetaSchema",
        "then": "CoreSchemaMetaSchema",
        "else": "CoreSchemaMetaSchema",
        "allOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "anyOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "oneOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "not": "CoreSchemaMetaSchema",
    },
    total=False,
)


_CORE_SCHEMA_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: Dict[str, Any] = {}
"""Default value of the field path 'Core schema meta-schema object definitions'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_ITEMS_DEFAULT = True
"""Default value of the field path 'Core schema meta-schema object items'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_MINLENGTH_ALLOF1_DEFAULT = 0
"""Default value of the field path 'Core schema meta-schema object minLength allof1'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
"""Default value of the field path 'Core schema meta-schema object patternProperties'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: Dict[str, Any] = {}
"""Default value of the field path 'Core schema meta-schema object properties'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
"""Default value of the field path 'Core schema meta-schema object readOnly'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_REQUIRED_DEFAULT: List[Any] = []
"""Default value of the field path 'Core schema meta-schema object required'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
"""Default value of the field path 'Core schema meta-schema object uniqueItems'"""


_CORE_SCHEMA_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
"""Default value of the field path 'Core schema meta-schema object writeOnly'"""


_CoreSchemaMetaSchemaObjectItemsAnyof1 = List["CoreSchemaMetaSchema"]
"""minItems: 1"""


_CoreSchemaMetaSchemaObjectMaxlength = int
"""minimum: 0"""


_CoreSchemaMetaSchemaObjectMinlength = Union[
    "_CoreSchemaMetaSchemaObjectMaxlength", "_CoreSchemaMetaSchemaObjectMinlengthAllof1"
]
"""
WARNING: PEP 544 does not support an Intersection type,
so `allOf` is interpreted as a `Union` for now.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
"""


_CoreSchemaMetaSchemaObjectMinlengthAllof1 = int
"""default: 0"""


_CoreSchemaMetaSchemaObjectRequired = List[str]
"""
uniqueItems: True
default:
  []
"""


_CoreSchemaMetaSchemaObjectTypeAnyof0 = Union[
    Literal["array"],
    Literal["boolean"],
    Literal["integer"],
    Literal["null"],
    Literal["number"],
    Literal["object"],
    Literal["string"],
]
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_ARRAY: Literal["array"] = "array"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_BOOLEAN: Literal["boolean"] = "boolean"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_INTEGER: Literal["integer"] = "integer"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_NULL: Literal["null"] = "null"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_NUMBER: Literal["number"] = "number"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_OBJECT: Literal["object"] = "object"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_STRING: Literal["string"] = "string"
"""The values for the '_CoreSchemaMetaSchemaObjectTypeAnyof0' enum"""


_CoreSchemaMetaSchemaObjectTypeAnyof1 = List["_CoreSchemaMetaSchemaObjectTypeAnyof0"]
"""
minItems: 1
uniqueItems: True
"""
