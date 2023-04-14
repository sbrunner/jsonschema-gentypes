"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
""" Applicator vocabulary meta-schema. """


JSONSchemaItemD2020 = TypedDict(
    "JSONSchemaItemD2020",
    {
        "prefixItems": "_SchemaArray",
        "items": "JSONSchemaD2020",
        "contains": "JSONSchemaD2020",
        "additionalProperties": "JSONSchemaD2020",
        # default:
        #   {}
        "properties": Dict[str, "JSONSchemaD2020"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": Dict[str, "JSONSchemaD2020"],
        # default:
        #   {}
        "dependentSchemas": Dict[str, "JSONSchemaD2020"],
        "propertyNames": "JSONSchemaD2020",
        "if": "JSONSchemaD2020",
        "then": "JSONSchemaD2020",
        "else": "JSONSchemaD2020",
        "allOf": "_SchemaArray",
        "anyOf": "_SchemaArray",
        "oneOf": "_SchemaArray",
        "not": "JSONSchemaD2020",
    },
    total=False,
)


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_DEPENDENTSCHEMAS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object dependentSchemas' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object patternProperties' """


_APPLICATOR_VOCABULARY_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Applicator vocabulary meta-schema object properties' """


_SchemaArray = List["JSONSchemaD2020"]
""" minItems: 1 """
