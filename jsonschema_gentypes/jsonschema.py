"""
Automatically generated file from a JSON schema.
"""


from enum import Enum
from typing import Any, Dict, List, TypedDict, Union

# Core schema meta-schema
#
# default: True
JSONSchema = Union["JSONSchemaItem", bool]


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
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "additionalItems": Dict[str, Any],
        # default: True
        "items": Union["_CoreSchemaMetaSchemaObjectItemsAnyof0", "_CoreSchemaMetaSchemaObjectItemsAnyof1"],
        "maxItems": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minItems": "_CoreSchemaMetaSchemaObjectMinlength",
        # default: False
        "uniqueItems": bool,
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "contains": Dict[str, Any],
        "maxProperties": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minProperties": "_CoreSchemaMetaSchemaObjectMinlength",
        "required": "_CoreSchemaMetaSchemaObjectRequired",
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "additionalProperties": Dict[str, Any],
        "definitions": Dict[str, "_CoreSchemaMetaSchemaObjectDefinitionsAdditionalproperties"],
        "properties": Dict[str, "_CoreSchemaMetaSchemaObjectPropertiesAdditionalproperties"],
        "patternProperties": Dict[str, "_CoreSchemaMetaSchemaObjectPatternpropertiesAdditionalproperties"],
        "dependencies": Dict[
            str,
            Union[
                "_CoreSchemaMetaSchemaObjectDependenciesAdditionalpropertiesAnyof0",
                "_CoreSchemaMetaSchemaObjectRequired",
            ],
        ],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "propertyNames": Dict[str, Any],
        "const": Any,
        # minItems: 1
        # uniqueItems: True
        "enum": List[Any],
        "type": Union["_CoreSchemaMetaSchemaObjectTypeAnyof0", "_CoreSchemaMetaSchemaObjectTypeAnyof1"],
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "if": Dict[str, Any],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "then": Dict[str, Any],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "else": Dict[str, Any],
        "allOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "anyOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "oneOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        # WARNING: Forward references may not be supported.
        # See: https://github.com/python/mypy/issues/731
        "not": Dict[str, Any],
    },
    total=False,
)


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectDefinitionsAdditionalproperties = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectDependenciesAdditionalpropertiesAnyof0 = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectItemsAnyof0 = Dict[str, Any]


# minItems: 1
_CoreSchemaMetaSchemaObjectItemsAnyof1 = List["_CoreSchemaMetaSchemaObjectItemsAnyof1Item"]


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectItemsAnyof1Item = Dict[str, Any]


# minimum: 0
_CoreSchemaMetaSchemaObjectMaxlength = int


# WARNING: PEP 544 does not support an Intersection type,
# so `allOf` is interpreted as a `Union` for now.
# See: https://github.com/python/typing/issues/213
_CoreSchemaMetaSchemaObjectMinlength = Union[
    "_CoreSchemaMetaSchemaObjectMaxlength", "_CoreSchemaMetaSchemaObjectMinlengthAllof1"
]


# default: 0
#
# WARNING: `default` keyword not supported.
# See: https://github.com/python/mypy/issues/6131
_CoreSchemaMetaSchemaObjectMinlengthAllof1 = int


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectPatternpropertiesAdditionalproperties = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/python/mypy/issues/731
_CoreSchemaMetaSchemaObjectPropertiesAdditionalproperties = Dict[str, Any]


# uniqueItems: True
_CoreSchemaMetaSchemaObjectRequired = List[str]


class _CoreSchemaMetaSchemaObjectTypeAnyof0(Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NULL = "null"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"


# minItems: 1
# uniqueItems: True
_CoreSchemaMetaSchemaObjectTypeAnyof1 = List["_CoreSchemaMetaSchemaObjectTypeAnyof0"]
