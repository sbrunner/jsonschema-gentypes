"""
Automatically generated file from a JSON schema.
"""


from typing import Dict, TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
""" Core vocabulary meta-schema. """


JSONSchemaItemD2020 = TypedDict(
    "JSONSchemaItemD2020",
    {
        "$id": "_UriReferenceString",
        "$schema": "_UriString",
        "$ref": "_UriReferenceString",
        "$anchor": "_AnchorString",
        "$dynamicRef": "_UriReferenceString",
        "$dynamicAnchor": "_AnchorString",
        # propertyNames:
        #   $ref: '#/$defs/uriString'
        "$vocabulary": Dict[str, bool],
        "$comment": str,
        "$defs": Dict[str, "JSONSchemaD2020"],
    },
    total=False,
)


_AnchorString = str
""" pattern: ^[A-Za-z_][-A-Za-z0-9._]*$ """


_UriReferenceString = str
""" format: uri-reference """


_UriString = str
""" format: uri """
