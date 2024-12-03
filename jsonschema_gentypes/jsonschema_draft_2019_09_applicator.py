"""Automatically generated file from a JSON schema."""

from typing import Any, TypedDict, Union

JSONSchemaD2019 = Union["JSONSchemaItemD2019", bool]
""" Applicator vocabulary meta-schema. """


JSONSchemaItemD2019 = TypedDict(
    "JSONSchemaItemD2019",
    {
        # Applicator vocabulary meta-schema.
        "additionalItems": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "unevaluatedItems": "JSONSchemaD2019",
        # Aggregation type: anyOf
        "items": "_ApplicatorVocabularyMetaSchemaObjectItems",
        # Applicator vocabulary meta-schema.
        "contains": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "additionalProperties": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "unevaluatedProperties": "JSONSchemaD2019",
        # default:
        #   {}
        "properties": dict[str, "JSONSchemaD2019"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchemaD2019"],
        "dependentSchemas": dict[str, "JSONSchemaD2019"],
        # Applicator vocabulary meta-schema.
        "propertyNames": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "if": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "then": "JSONSchemaD2019",
        # Applicator vocabulary meta-schema.
        "else": "JSONSchemaD2019",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Applicator vocabulary meta-schema.
        "not": "JSONSchemaD2019",
    },
    total=False,
)


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


_ApplicatorVocabularyMetaSchemaObjectItems = Union["JSONSchemaD2019", "_SchemaArray"]
""" Aggregation type: anyOf """


_SchemaArray = list["JSONSchemaD2019"]
""" minItems: 1 """
