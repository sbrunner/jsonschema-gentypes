"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, Literal, TypedDict, Union

ApplicatorVocabularyMetaSchema = Union["_ApplicatorVocabularyMetaSchemaObject", bool]
""" Applicator vocabulary meta-schema. """


ContentVocabularyMetaSchema = Union["_ContentVocabularyMetaSchemaObject", bool]
""" Content vocabulary meta-schema. """


CoreAndValidationSpecificationsMetaSchema = Union[
    "CoreVocabularyMetaSchema",
    "ApplicatorVocabularyMetaSchema",
    "UnevaluatedApplicatorVocabularyMetaSchema",
    "ValidationVocabularyMetaSchema",
    "MetaDataVocabularyMetaSchema",
    "FormatVocabularyMetaSchemaForAnnotationResults",
    "ContentVocabularyMetaSchema",
]
"""
Core and Validation specifications meta-schema.

$comment: This meta-schema also defines keywords that have appeared in previous drafts in order to prevent incompatible extensions as they remain in common use.

WARNING: PEP 544 does not support an Intersection type,
so `allOf` is interpreted as a `Union` for now.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/8

Aggregation type: allOf
"""


CoreVocabularyMetaSchema = Union["_CoreVocabularyMetaSchemaObject", bool]
""" Core vocabulary meta-schema. """


FormatVocabularyMetaSchemaForAnnotationResults = Union[
    "_FormatVocabularyMetaSchemaForAnnotationResultsObject", bool
]
""" Format vocabulary meta-schema for annotation results. """


MetaDataVocabularyMetaSchema = Union["_MetaDataVocabularyMetaSchemaObject", bool]
""" Meta-data vocabulary meta-schema. """


UnevaluatedApplicatorVocabularyMetaSchema = Union["_UnevaluatedApplicatorVocabularyMetaSchemaObject", bool]
""" Unevaluated applicator vocabulary meta-schema. """


ValidationVocabularyMetaSchema = Union["_ValidationVocabularyMetaSchemaObject", bool]
""" Validation vocabulary meta-schema. """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_DEPENDENTSCHEMAS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object dependentSchemas' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


_AnchorString = str
""" pattern: ^[A-Za-z_][-A-Za-z0-9._]*$ """


_ApplicatorVocabularyMetaSchemaObject = TypedDict(
    "_ApplicatorVocabularyMetaSchemaObject",
    {
        # minItems: 1
        "prefixItems": "_SchemaArray",
        # Applicator vocabulary meta-schema.
        "items": "ApplicatorVocabularyMetaSchema",
        # Applicator vocabulary meta-schema.
        "contains": "ApplicatorVocabularyMetaSchema",
        # Applicator vocabulary meta-schema.
        "additionalProperties": "ApplicatorVocabularyMetaSchema",
        # default:
        #   {}
        "properties": Dict[str, "ApplicatorVocabularyMetaSchema"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "ApplicatorVocabularyMetaSchema"],
        # default:
        #   {}
        "dependentSchemas": Dict[str, "ApplicatorVocabularyMetaSchema"],
        # Applicator vocabulary meta-schema.
        "propertyNames": "ApplicatorVocabularyMetaSchema",
        # Applicator vocabulary meta-schema.
        "if": "ApplicatorVocabularyMetaSchema",
        # Applicator vocabulary meta-schema.
        "then": "ApplicatorVocabularyMetaSchema",
        # Applicator vocabulary meta-schema.
        "else": "ApplicatorVocabularyMetaSchema",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Applicator vocabulary meta-schema.
        "not": "ApplicatorVocabularyMetaSchema",
    },
    total=False,
)


class _ContentVocabularyMetaSchemaObject(TypedDict, total=False):
    contentEncoding: str
    contentMediaType: str
    contentSchema: "ContentVocabularyMetaSchema"
    """ Content vocabulary meta-schema. """


_CoreVocabularyMetaSchemaObject = TypedDict(
    "_CoreVocabularyMetaSchemaObject",
    {
        # format: uri-reference
        "$id": "_UriReferenceString",
        # format: uri
        "$schema": "_UriString",
        # format: uri-reference
        "$ref": "_UriReferenceString",
        # pattern: ^[A-Za-z_][-A-Za-z0-9._]*$
        "$anchor": "_AnchorString",
        # format: uri-reference
        "$dynamicRef": "_UriReferenceString",
        # pattern: ^[A-Za-z_][-A-Za-z0-9._]*$
        "$dynamicAnchor": "_AnchorString",
        # propertyNames:
        #   $ref: '#/$defs/uriString'
        "$vocabulary": Dict[str, bool],
        "$comment": str,
        "$defs": Dict[str, "CoreVocabularyMetaSchema"],
    },
    total=False,
)


class _FormatVocabularyMetaSchemaForAnnotationResultsObject(TypedDict, total=False):
    format: str


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object deprecated' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object readOnly' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object writeOnly' """


class _MetaDataVocabularyMetaSchemaObject(TypedDict, total=False):
    title: str
    description: str
    default: Any
    deprecated: bool
    """ default: False """

    readOnly: bool
    """ default: False """

    writeOnly: bool
    """ default: False """

    examples: List[Any]
    """ items: True """


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_STRING_ARRAY_DEFAULT: List[Any] = []
""" Default value of the field path 'string array' """


_SchemaArray = List["ApplicatorVocabularyMetaSchema"]
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


class _UnevaluatedApplicatorVocabularyMetaSchemaObject(TypedDict, total=False):
    unevaluatedItems: "UnevaluatedApplicatorVocabularyMetaSchema"
    """ Unevaluated applicator vocabulary meta-schema. """

    unevaluatedProperties: "UnevaluatedApplicatorVocabularyMetaSchema"
    """ Unevaluated applicator vocabulary meta-schema. """


_UriReferenceString = str
""" format: uri-reference """


_UriString = str
""" format: uri """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
""" Default value of the field path 'Validation vocabulary meta-schema object minContains' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINLENGTH_DEFAULT = 0
""" Default value of the field path 'Validation vocabulary meta-schema object minLength' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_REQUIRED_DEFAULT: List[Any] = []
""" Default value of the field path 'Validation vocabulary meta-schema object required' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Validation vocabulary meta-schema object uniqueItems' """


class _ValidationVocabularyMetaSchemaObject(TypedDict, total=False):
    type: "_ValidationVocabularyMetaSchemaObjectType"
    """ Aggregation type: anyOf """

    const: Any
    enum: List[Any]
    """ items: True """

    multipleOf: Union[int, float]
    """ exclusiveMinimum: 0 """

    maximum: Union[int, float]
    exclusiveMaximum: Union[int, float]
    minimum: Union[int, float]
    exclusiveMinimum: Union[int, float]
    maxLength: "_NonNegativeInteger"
    """ minimum: 0 """

    minLength: "_NonNegativeInteger"
    """ minimum: 0 """

    pattern: str
    """ format: regex """

    maxItems: "_NonNegativeInteger"
    """ minimum: 0 """

    minItems: "_NonNegativeInteger"
    """ minimum: 0 """

    uniqueItems: bool
    """ default: False """

    maxContains: "_NonNegativeInteger"
    """ minimum: 0 """

    minContains: "_NonNegativeInteger"
    """ minimum: 0 """

    maxProperties: "_NonNegativeInteger"
    """ minimum: 0 """

    minProperties: "_NonNegativeInteger"
    """ minimum: 0 """

    required: "_StringArray"
    """
    uniqueItems: True
    default:
      []
    """

    dependentRequired: Dict[str, "_StringArray"]


_ValidationVocabularyMetaSchemaObjectType = Union[
    "_SimpleTypes", "_ValidationVocabularyMetaSchemaObjectTypeAnyof1"
]
""" Aggregation type: anyOf """


_ValidationVocabularyMetaSchemaObjectTypeAnyof1 = List["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""
