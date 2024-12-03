"""Automatically generated file from a JSON schema."""

from typing import Any, TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
""" Applicator vocabulary meta-schema. """


JSONSchemaItemD2020 = TypedDict(
    "JSONSchemaItemD2020",
    {
        # minItems: 1
        "prefixItems": "_SchemaArray",
        # Applicator vocabulary meta-schema.
        "items": "JSONSchemaD2020",
        # Applicator vocabulary meta-schema.
        "contains": "JSONSchemaD2020",
        # Applicator vocabulary meta-schema.
        "additionalProperties": "JSONSchemaD2020",
        # default:
        #   {}
        "properties": dict[str, "JSONSchemaD2020"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchemaD2020"],
        # default:
        #   {}
        "dependentSchemas": dict[str, "JSONSchemaD2020"],
        # Applicator vocabulary meta-schema.
        "propertyNames": "JSONSchemaD2020",
        # Applicator vocabulary meta-schema.
        "if": "JSONSchemaD2020",
        # Applicator vocabulary meta-schema.
        "then": "JSONSchemaD2020",
        # Applicator vocabulary meta-schema.
        "else": "JSONSchemaD2020",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Applicator vocabulary meta-schema.
        "not": "JSONSchemaD2020",
    },
    total=False,
)


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_DEPENDENTSCHEMAS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object dependentSchemas' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


_SchemaArray = list["JSONSchemaD2020"]
""" minItems: 1 """
