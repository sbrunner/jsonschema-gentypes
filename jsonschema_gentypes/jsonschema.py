"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

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
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "additionalItems": Dict[str, Any],
        # default: True
        "items": Union["_CoreSchemaMetaSchemaObjectItemsAnyof0", "_CoreSchemaMetaSchemaObjectItemsAnyof1"],
        "maxItems": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minItems": "_CoreSchemaMetaSchemaObjectMinlength",
        # default: False
        "uniqueItems": bool,
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "contains": Dict[str, Any],
        "maxProperties": "_CoreSchemaMetaSchemaObjectMaxlength",
        "minProperties": "_CoreSchemaMetaSchemaObjectMinlength",
        "required": "_CoreSchemaMetaSchemaObjectRequired",
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "additionalProperties": Dict[str, Any],
        # default:
        #   {}
        "definitions": Dict[str, "_CoreSchemaMetaSchemaObjectDefinitionsAdditionalproperties"],
        # default:
        #   {}
        "properties": Dict[str, "_CoreSchemaMetaSchemaObjectPropertiesAdditionalproperties"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "_CoreSchemaMetaSchemaObjectPatternpropertiesAdditionalproperties"],
        "dependencies": Dict[
            str,
            Union[
                "_CoreSchemaMetaSchemaObjectDependenciesAdditionalpropertiesAnyof0",
                "_CoreSchemaMetaSchemaObjectRequired",
            ],
        ],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
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
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "if": Dict[str, Any],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "then": Dict[str, Any],
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "else": Dict[str, Any],
        "allOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "anyOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        "oneOf": "_CoreSchemaMetaSchemaObjectItemsAnyof1",
        # WARNING: Forward references may not be supported.
        # See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
        "not": Dict[str, Any],
    },
    total=False,
)


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectDefinitionsAdditionalproperties = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectDependenciesAdditionalpropertiesAnyof0 = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectItemsAnyof0 = Dict[str, Any]


# minItems: 1
_CoreSchemaMetaSchemaObjectItemsAnyof1 = List["_CoreSchemaMetaSchemaObjectItemsAnyof1Item"]


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectItemsAnyof1Item = Dict[str, Any]


# minimum: 0
_CoreSchemaMetaSchemaObjectMaxlength = int


# WARNING: PEP 544 does not support an Intersection type,
# so `allOf` is interpreted as a `Union` for now.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
_CoreSchemaMetaSchemaObjectMinlength = Union[
    "_CoreSchemaMetaSchemaObjectMaxlength", "_CoreSchemaMetaSchemaObjectMinlengthAllof1"
]


# default: 0
_CoreSchemaMetaSchemaObjectMinlengthAllof1 = int


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectPatternpropertiesAdditionalproperties = Dict[str, Any]


# WARNING: Forward references may not be supported.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/9
_CoreSchemaMetaSchemaObjectPropertiesAdditionalproperties = Dict[str, Any]


# uniqueItems: True
# default:
#   []
_CoreSchemaMetaSchemaObjectRequired = List[str]


_CoreSchemaMetaSchemaObjectTypeAnyof0 = Union[
    Literal["array"],
    Literal["boolean"],
    Literal["integer"],
    Literal["null"],
    Literal["number"],
    Literal["object"],
    Literal["string"],
]
# The values for the enum
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_ARRAY: Literal["array"] = "array"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_BOOLEAN: Literal["boolean"] = "boolean"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_INTEGER: Literal["integer"] = "integer"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_NULL: Literal["null"] = "null"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_NUMBER: Literal["number"] = "number"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_OBJECT: Literal["object"] = "object"
_CORESCHEMAMETASCHEMAOBJECTTYPEANYOF0_STRING: Literal["string"] = "string"


# minItems: 1
# uniqueItems: True
_CoreSchemaMetaSchemaObjectTypeAnyof1 = List["_CoreSchemaMetaSchemaObjectTypeAnyof0"]
