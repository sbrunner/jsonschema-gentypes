"""Automatically generated file from a JSON schema."""

from typing import Any, Literal, TypedDict, Union

ContentVocabularyMetaSchema = Union["_ContentVocabularyMetaSchemaObject", bool]
""" Content vocabulary meta-schema. """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
""" Default value of the field path 'Content vocabulary meta-schema object deprecated' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
""" Default value of the field path 'Content vocabulary meta-schema object minContains' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Content vocabulary meta-schema object patternProperties' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Content vocabulary meta-schema object properties' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
""" Default value of the field path 'Content vocabulary meta-schema object readOnly' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Content vocabulary meta-schema object uniqueItems' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
""" Default value of the field path 'Content vocabulary meta-schema object writeOnly' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT__DEFS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Content vocabulary meta-schema object $defs' """


_CONTENT_VOCABULARY_META_SCHEMA_OBJECT__RECURSIVEANCHOR_DEFAULT = False
""" Default value of the field path 'Content vocabulary meta-schema object $recursiveAnchor' """


_ContentVocabularyMetaSchemaObject = TypedDict(
    "_ContentVocabularyMetaSchemaObject",
    {
        # format: uri-reference
        # $comment: Non-empty fragments not allowed.
        # pattern: ^[^#]*#?$
        "$id": str,
        # format: uri
        "$schema": str,
        # pattern: ^[A-Za-z][-A-Za-z0-9.:_]*$
        "$anchor": str,
        # format: uri-reference
        "$ref": str,
        # format: uri-reference
        "$recursiveRef": str,
        # default: False
        "$recursiveAnchor": bool,
        # propertyNames:
        #   __type__: string
        #   format: uri
        "$vocabulary": dict[str, bool],
        "$comment": str,
        # default:
        #   {}
        "$defs": dict[str, "ContentVocabularyMetaSchema"],
        # Content vocabulary meta-schema.
        "additionalItems": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "unevaluatedItems": "ContentVocabularyMetaSchema",
        # Aggregation type: anyOf
        "items": "_ContentVocabularyMetaSchemaObjectItems",
        # Content vocabulary meta-schema.
        "contains": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "additionalProperties": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "unevaluatedProperties": "ContentVocabularyMetaSchema",
        # default:
        #   {}
        "properties": dict[str, "ContentVocabularyMetaSchema"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "ContentVocabularyMetaSchema"],
        "dependentSchemas": dict[str, "ContentVocabularyMetaSchema"],
        # Content vocabulary meta-schema.
        "propertyNames": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "if": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "then": "ContentVocabularyMetaSchema",
        # Content vocabulary meta-schema.
        "else": "ContentVocabularyMetaSchema",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Content vocabulary meta-schema.
        "not": "ContentVocabularyMetaSchema",
        # exclusiveMinimum: 0
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        "exclusiveMaximum": Union[int, float],
        "minimum": Union[int, float],
        "exclusiveMinimum": Union[int, float],
        # minimum: 0
        "maxLength": "_NonNegativeInteger",
        # minimum: 0
        "minLength": "_NonNegativeInteger",
        # format: regex
        "pattern": str,
        # minimum: 0
        "maxItems": "_NonNegativeInteger",
        # minimum: 0
        "minItems": "_NonNegativeInteger",
        # default: False
        "uniqueItems": bool,
        # minimum: 0
        "maxContains": "_NonNegativeInteger",
        # minimum: 0
        "minContains": "_NonNegativeInteger",
        # minimum: 0
        "maxProperties": "_NonNegativeInteger",
        # minimum: 0
        "minProperties": "_NonNegativeInteger",
        # uniqueItems: True
        # default:
        #   []
        "required": "_StringArray",
        "dependentRequired": dict[str, "_StringArray"],
        "const": Any,
        "enum": list[Any],
        # Aggregation type: anyOf
        "type": "_ContentVocabularyMetaSchemaObjectType",
        "title": str,
        "description": str,
        "default": Any,
        # default: False
        "deprecated": bool,
        # default: False
        "readOnly": bool,
        # default: False
        "writeOnly": bool,
        "examples": list[Any],
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        # Content vocabulary meta-schema.
        "contentSchema": "ContentVocabularyMetaSchema",
    },
    total=False,
)


_ContentVocabularyMetaSchemaObjectItems = Union["ContentVocabularyMetaSchema", "_SchemaArray"]
""" Aggregation type: anyOf """


_ContentVocabularyMetaSchemaObjectType = Union["_SimpleTypes", "_ContentVocabularyMetaSchemaObjectTypeAnyof1"]
""" Aggregation type: anyOf """


_ContentVocabularyMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_STRING_ARRAY_DEFAULT: list[Any] = []
""" Default value of the field path 'string array' """


_SchemaArray = list["ContentVocabularyMetaSchema"]
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
