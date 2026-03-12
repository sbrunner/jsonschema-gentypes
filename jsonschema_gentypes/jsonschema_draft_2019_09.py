"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict, Union

ApplicatorVocabularyMetaSchema = Union["_ApplicatorVocabularyMetaSchemaObject", bool]
r"""
Applicator vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


ContentVocabularyMetaSchema = Union["_ContentVocabularyMetaSchemaObject", bool]
r"""
Content vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


CoreAndValidationSpecificationsMetaSchema = Union["_CoreAndValidationSpecificationsMetaSchemaObject", bool]
r"""
Core and Validation specifications meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
"""


CoreVocabularyMetaSchema = Union["_CoreVocabularyMetaSchemaObject", bool]
r"""
Core vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


FormatVocabularyMetaSchema = Union["_FormatVocabularyMetaSchemaObject", bool]
r"""
Format vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


MetaDataVocabularyMetaSchema = Union["_MetaDataVocabularyMetaSchemaObject", bool]
r"""
Meta-data vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


ValidationVocabularyMetaSchema = Union["_ValidationVocabularyMetaSchemaObject", bool]
r"""
Validation vocabulary meta-schema.

$vocabulary:
  https://json-schema.org/draft/2019-09/vocab/applicator: true
  https://json-schema.org/draft/2019-09/vocab/content: true
  https://json-schema.org/draft/2019-09/vocab/core: true
  https://json-schema.org/draft/2019-09/vocab/format: false
  https://json-schema.org/draft/2019-09/vocab/meta-data: true
  https://json-schema.org/draft/2019-09/vocab/validation: true
"""


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


# | $vocabulary:
# |   https://json-schema.org/draft/2019-09/vocab/applicator: true
# |   https://json-schema.org/draft/2019-09/vocab/content: true
# |   https://json-schema.org/draft/2019-09/vocab/core: true
# |   https://json-schema.org/draft/2019-09/vocab/format: false
# |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
# |   https://json-schema.org/draft/2019-09/vocab/validation: true
_ApplicatorVocabularyMetaSchemaObject = TypedDict(
    "_ApplicatorVocabularyMetaSchemaObject",
    {
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "additionalItems": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "unevaluatedItems": "ApplicatorVocabularyMetaSchema",
        # | Aggregation type: anyOf
        "items": "_ApplicatorVocabularyMetaSchemaObjectItems",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "contains": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "additionalProperties": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "unevaluatedProperties": "ApplicatorVocabularyMetaSchema",
        # | default:
        # |   {}
        "properties": dict[str, "ApplicatorVocabularyMetaSchema"],
        # | propertyNames:
        # |   format: regex
        # | default:
        # |   {}
        "patternProperties": dict[str, "ApplicatorVocabularyMetaSchema"],
        "dependentSchemas": dict[str, "ApplicatorVocabularyMetaSchema"],
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "propertyNames": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "if": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "then": "ApplicatorVocabularyMetaSchema",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "else": "ApplicatorVocabularyMetaSchema",
        # | minItems: 1
        "allOf": "_SchemaArray",
        # | minItems: 1
        "anyOf": "_SchemaArray",
        # | minItems: 1
        "oneOf": "_SchemaArray",
        # | Applicator vocabulary meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        "not": "ApplicatorVocabularyMetaSchema",
    },
    total=False,
)


_ApplicatorVocabularyMetaSchemaObjectItems = Union["ApplicatorVocabularyMetaSchema", "_SchemaArray"]
r""" Aggregation type: anyOf """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Core and Validation specifications meta-schema object definitions' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
r""" Default value of the field path 'Core and Validation specifications meta-schema object deprecated' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
r""" Default value of the field path 'Core and Validation specifications meta-schema object minContains' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Core and Validation specifications meta-schema object patternProperties' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Core and Validation specifications meta-schema object properties' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
r""" Default value of the field path 'Core and Validation specifications meta-schema object readOnly' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
r""" Default value of the field path 'Core and Validation specifications meta-schema object uniqueItems' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
r""" Default value of the field path 'Core and Validation specifications meta-schema object writeOnly' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT__DEFS_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Core and Validation specifications meta-schema object $defs' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT__RECURSIVEANCHOR_DEFAULT = False
r""" Default value of the field path 'Core and Validation specifications meta-schema object $recursiveAnchor' """


_CORE_VOCABULARY_META_SCHEMA_OBJECT__DEFS_DEFAULT: dict[str, Any] = {}
r""" Default value of the field path 'Core vocabulary meta-schema object $defs' """


_CORE_VOCABULARY_META_SCHEMA_OBJECT__RECURSIVEANCHOR_DEFAULT = False
r""" Default value of the field path 'Core vocabulary meta-schema object $recursiveAnchor' """


class _ContentVocabularyMetaSchemaObject(TypedDict, total=False):
    r"""
    $vocabulary:
      https://json-schema.org/draft/2019-09/vocab/applicator: true
      https://json-schema.org/draft/2019-09/vocab/content: true
      https://json-schema.org/draft/2019-09/vocab/core: true
      https://json-schema.org/draft/2019-09/vocab/format: false
      https://json-schema.org/draft/2019-09/vocab/meta-data: true
      https://json-schema.org/draft/2019-09/vocab/validation: true
    """

    contentMediaType: str
    contentEncoding: str
    contentSchema: "ContentVocabularyMetaSchema"
    r"""
    Content vocabulary meta-schema.

    $vocabulary:
      https://json-schema.org/draft/2019-09/vocab/applicator: true
      https://json-schema.org/draft/2019-09/vocab/content: true
      https://json-schema.org/draft/2019-09/vocab/core: true
      https://json-schema.org/draft/2019-09/vocab/format: false
      https://json-schema.org/draft/2019-09/vocab/meta-data: true
      https://json-schema.org/draft/2019-09/vocab/validation: true
    """


# | $vocabulary:
# |   https://json-schema.org/draft/2019-09/vocab/applicator: true
# |   https://json-schema.org/draft/2019-09/vocab/content: true
# |   https://json-schema.org/draft/2019-09/vocab/core: true
# |   https://json-schema.org/draft/2019-09/vocab/format: false
# |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
# |   https://json-schema.org/draft/2019-09/vocab/validation: true
_CoreAndValidationSpecificationsMetaSchemaObject = TypedDict(
    "_CoreAndValidationSpecificationsMetaSchemaObject",
    {
        # | $comment: While no longer an official keyword as it is replaced by $defs, this keyword is retained in the meta-schema to prevent incompatible extensions as it remains in common use.
        # | default:
        # |   {}
        "definitions": dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        # | $comment: "dependencies" is no longer a keyword, but schema authors should avoid redefining it to facilitate a smooth transition to "dependentSchemas" and "dependentRequired"
        "dependencies": dict[
            str, "_CoreAndValidationSpecificationsMetaSchemaObjectDependenciesAdditionalproperties"
        ],
        # | format: uri-reference
        # | $comment: Non-empty fragments not allowed.
        # | pattern: ^[^#]*#?$
        "$id": str,
        # | format: uri
        "$schema": str,
        # | pattern: ^[A-Za-z][-A-Za-z0-9.:_]*$
        "$anchor": str,
        # | format: uri-reference
        "$ref": str,
        # | format: uri-reference
        "$recursiveRef": str,
        # | default: False
        "$recursiveAnchor": bool,
        # | propertyNames:
        # |   __type__: string
        # |   format: uri
        "$vocabulary": dict[str, bool],
        "$comment": str,
        # | default:
        # |   {}
        "$defs": dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "additionalItems": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "unevaluatedItems": "CoreAndValidationSpecificationsMetaSchema",
        # | Aggregation type: anyOf
        "items": "_CoreAndValidationSpecificationsMetaSchemaObjectItems",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "contains": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "additionalProperties": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "unevaluatedProperties": "CoreAndValidationSpecificationsMetaSchema",
        # | default:
        # |   {}
        "properties": dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        # | propertyNames:
        # |   format: regex
        # | default:
        # |   {}
        "patternProperties": dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        "dependentSchemas": dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "propertyNames": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "if": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "then": "CoreAndValidationSpecificationsMetaSchema",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "else": "CoreAndValidationSpecificationsMetaSchema",
        # | minItems: 1
        "allOf": "_SchemaArray",
        # | minItems: 1
        "anyOf": "_SchemaArray",
        # | minItems: 1
        "oneOf": "_SchemaArray",
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "not": "CoreAndValidationSpecificationsMetaSchema",
        # | exclusiveMinimum: 0
        "multipleOf": int | float,
        "maximum": int | float,
        "exclusiveMaximum": int | float,
        "minimum": int | float,
        "exclusiveMinimum": int | float,
        # | minimum: 0
        "maxLength": "_NonNegativeInteger",
        # | minimum: 0
        "minLength": "_NonNegativeInteger",
        # | format: regex
        "pattern": str,
        # | minimum: 0
        "maxItems": "_NonNegativeInteger",
        # | minimum: 0
        "minItems": "_NonNegativeInteger",
        # | default: False
        "uniqueItems": bool,
        # | minimum: 0
        "maxContains": "_NonNegativeInteger",
        # | minimum: 0
        "minContains": "_NonNegativeInteger",
        # | minimum: 0
        "maxProperties": "_NonNegativeInteger",
        # | minimum: 0
        "minProperties": "_NonNegativeInteger",
        # | uniqueItems: True
        # | default:
        # |   []
        "required": "_StringArray",
        "dependentRequired": dict[str, "_StringArray"],
        "const": Any,
        "enum": list[Any],
        # | Aggregation type: anyOf
        "type": "_CoreAndValidationSpecificationsMetaSchemaObjectType",
        "title": str,
        "description": str,
        "default": Any,
        # | default: False
        "deprecated": bool,
        # | default: False
        "readOnly": bool,
        # | default: False
        "writeOnly": bool,
        "examples": list[Any],
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        # | Core and Validation specifications meta-schema.
        # |
        # | $vocabulary:
        # |   https://json-schema.org/draft/2019-09/vocab/applicator: true
        # |   https://json-schema.org/draft/2019-09/vocab/content: true
        # |   https://json-schema.org/draft/2019-09/vocab/core: true
        # |   https://json-schema.org/draft/2019-09/vocab/format: false
        # |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
        # |   https://json-schema.org/draft/2019-09/vocab/validation: true
        # | Subtype: "CoreVocabularyMetaSchema", "ApplicatorVocabularyMetaSchema", "ValidationVocabularyMetaSchema", "MetaDataVocabularyMetaSchema", "FormatVocabularyMetaSchema", "ContentVocabularyMetaSchema"
        "contentSchema": "CoreAndValidationSpecificationsMetaSchema",
    },
    total=False,
)


_CoreAndValidationSpecificationsMetaSchemaObjectDependenciesAdditionalproperties = Union[
    "CoreAndValidationSpecificationsMetaSchema", "_MetaValidationNumberSignDefsStringarray"
]
r""" Aggregation type: anyOf """


_CoreAndValidationSpecificationsMetaSchemaObjectItems = Union[
    "CoreAndValidationSpecificationsMetaSchema", "_SchemaArray"
]
r""" Aggregation type: anyOf """


_CoreAndValidationSpecificationsMetaSchemaObjectType = Union[
    "_SimpleTypes", "_CoreAndValidationSpecificationsMetaSchemaObjectTypeAnyof1"
]
r""" Aggregation type: anyOf """


_CoreAndValidationSpecificationsMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
r"""
minItems: 1
uniqueItems: True
"""


# | $vocabulary:
# |   https://json-schema.org/draft/2019-09/vocab/applicator: true
# |   https://json-schema.org/draft/2019-09/vocab/content: true
# |   https://json-schema.org/draft/2019-09/vocab/core: true
# |   https://json-schema.org/draft/2019-09/vocab/format: false
# |   https://json-schema.org/draft/2019-09/vocab/meta-data: true
# |   https://json-schema.org/draft/2019-09/vocab/validation: true
_CoreVocabularyMetaSchemaObject = TypedDict(
    "_CoreVocabularyMetaSchemaObject",
    {
        # | format: uri-reference
        # | $comment: Non-empty fragments not allowed.
        # | pattern: ^[^#]*#?$
        "$id": str,
        # | format: uri
        "$schema": str,
        # | pattern: ^[A-Za-z][-A-Za-z0-9.:_]*$
        "$anchor": str,
        # | format: uri-reference
        "$ref": str,
        # | format: uri-reference
        "$recursiveRef": str,
        # | default: False
        "$recursiveAnchor": bool,
        # | propertyNames:
        # |   __type__: string
        # |   format: uri
        "$vocabulary": dict[str, bool],
        "$comment": str,
        # | default:
        # |   {}
        "$defs": dict[str, "CoreVocabularyMetaSchema"],
    },
    total=False,
)


class _FormatVocabularyMetaSchemaObject(TypedDict, total=False):
    r"""
    $vocabulary:
      https://json-schema.org/draft/2019-09/vocab/applicator: true
      https://json-schema.org/draft/2019-09/vocab/content: true
      https://json-schema.org/draft/2019-09/vocab/core: true
      https://json-schema.org/draft/2019-09/vocab/format: false
      https://json-schema.org/draft/2019-09/vocab/meta-data: true
      https://json-schema.org/draft/2019-09/vocab/validation: true
    """

    format: str


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object deprecated' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object readOnly' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object writeOnly' """


_META_VALIDATION_NUMBER_SIGN___DEFS_STRINGARRAY_DEFAULT: list[Any] = []
r""" Default value of the field path 'meta validation# $defs stringArray' """


class _MetaDataVocabularyMetaSchemaObject(TypedDict, total=False):
    r"""
    $vocabulary:
      https://json-schema.org/draft/2019-09/vocab/applicator: true
      https://json-schema.org/draft/2019-09/vocab/content: true
      https://json-schema.org/draft/2019-09/vocab/core: true
      https://json-schema.org/draft/2019-09/vocab/format: false
      https://json-schema.org/draft/2019-09/vocab/meta-data: true
      https://json-schema.org/draft/2019-09/vocab/validation: true
    """

    title: str
    description: str
    default: Any
    deprecated: bool
    r""" default: False """

    readOnly: bool
    r""" default: False """

    writeOnly: bool
    r""" default: False """

    examples: list[Any]


_MetaValidationNumberSignDefsStringarray = list[str]
r"""
uniqueItems: True
default:
  []
"""


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
r""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
r""" minimum: 0 """


_STRING_ARRAY_DEFAULT: list[Any] = []
r""" Default value of the field path 'string array' """


_SchemaArray = list["ApplicatorVocabularyMetaSchema"]
r""" minItems: 1 """


_SimpleTypes = Literal["array", "boolean", "integer", "null", "number", "object", "string"]
_SIMPLETYPES_ARRAY: Literal["array"] = "array"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_BOOLEAN: Literal["boolean"] = "boolean"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_INTEGER: Literal["integer"] = "integer"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NULL: Literal["null"] = "null"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NUMBER: Literal["number"] = "number"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_OBJECT: Literal["object"] = "object"
r"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_STRING: Literal["string"] = "string"
r"""The values for the '_SimpleTypes' enum"""


_StringArray = list[str]
r"""
uniqueItems: True
default:
  []
"""


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_MINCONTAINS_DEFAULT = 1
r""" Default value of the field path 'Validation vocabulary meta-schema object minContains' """


_VALIDATION_VOCABULARY_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
r""" Default value of the field path 'Validation vocabulary meta-schema object uniqueItems' """


class _ValidationVocabularyMetaSchemaObject(TypedDict, total=False):
    r"""
    $vocabulary:
      https://json-schema.org/draft/2019-09/vocab/applicator: true
      https://json-schema.org/draft/2019-09/vocab/content: true
      https://json-schema.org/draft/2019-09/vocab/core: true
      https://json-schema.org/draft/2019-09/vocab/format: false
      https://json-schema.org/draft/2019-09/vocab/meta-data: true
      https://json-schema.org/draft/2019-09/vocab/validation: true
    """

    multipleOf: int | float
    r""" exclusiveMinimum: 0 """

    maximum: int | float
    exclusiveMaximum: int | float
    minimum: int | float
    exclusiveMinimum: int | float
    maxLength: "_NonNegativeInteger"
    r""" minimum: 0 """

    minLength: "_NonNegativeInteger"
    r""" minimum: 0 """

    pattern: str
    r""" format: regex """

    maxItems: "_NonNegativeInteger"
    r""" minimum: 0 """

    minItems: "_NonNegativeInteger"
    r""" minimum: 0 """

    uniqueItems: bool
    r""" default: False """

    maxContains: "_NonNegativeInteger"
    r""" minimum: 0 """

    minContains: "_NonNegativeInteger"
    r""" minimum: 0 """

    maxProperties: "_NonNegativeInteger"
    r""" minimum: 0 """

    minProperties: "_NonNegativeInteger"
    r""" minimum: 0 """

    required: "_StringArray"
    r"""
    uniqueItems: True
    default:
      []
    """

    dependentRequired: dict[str, "_StringArray"]
    const: Any
    enum: list[Any]
    type: "_ValidationVocabularyMetaSchemaObjectType"
    r""" Aggregation type: anyOf """


_ValidationVocabularyMetaSchemaObjectType = Union[
    "_SimpleTypes", "_ValidationVocabularyMetaSchemaObjectTypeAnyof1"
]
r""" Aggregation type: anyOf """


_ValidationVocabularyMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
r"""
minItems: 1
uniqueItems: True
"""
