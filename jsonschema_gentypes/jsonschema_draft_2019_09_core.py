"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, TypedDict, Union

JSONSchemaD2019 = Union["JSONSchemaItemD2019", bool]
""" Core vocabulary meta-schema. """


JSONSchemaItemD2019 = TypedDict(
    "JSONSchemaItemD2019",
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
        "$vocabulary": Dict[str, bool],
        "$comment": str,
        # default:
        #   {}
        "$defs": Dict[str, "JSONSchemaD2019"],
    },
    total=False,
)


_CORE_VOCABULARY_META_SCHEMA_OBJECT__DEFS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core vocabulary meta-schema object $defs' """


_CORE_VOCABULARY_META_SCHEMA_OBJECT__RECURSIVEANCHOR_DEFAULT = False
""" Default value of the field path 'Core vocabulary meta-schema object $recursiveAnchor' """
