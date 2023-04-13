"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, TypedDict, Union

JSONSchemaD2019 = Union["JSONSchemaItemD2019", bool]
""" Applicator vocabulary meta-schema. """


JSONSchemaItemD2019 = TypedDict(
    "JSONSchemaItemD2019",
    {
        "additionalItems": "JSONSchemaD2019",
        "unevaluatedItems": "JSONSchemaD2019",
        "items": Union["JSONSchemaD2019", "_SchemaArray"],
        "contains": "JSONSchemaD2019",
        "additionalProperties": "JSONSchemaD2019",
        "unevaluatedProperties": "JSONSchemaD2019",
        # default:
        #   {}
        "properties": Dict[str, "JSONSchemaD2019"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "JSONSchemaD2019"],
        "dependentSchemas": Dict[str, "JSONSchemaD2019"],
        "propertyNames": "JSONSchemaD2019",
        "if": "JSONSchemaD2019",
        "then": "JSONSchemaD2019",
        "else": "JSONSchemaD2019",
        "allOf": "_SchemaArray",
        "anyOf": "_SchemaArray",
        "oneOf": "_SchemaArray",
        "not": "JSONSchemaD2019",
    },
    total=False,
)


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


_SchemaArray = List["JSONSchemaD2019"]
""" minItems: 1 """
