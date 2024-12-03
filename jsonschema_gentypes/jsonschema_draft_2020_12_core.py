"""Automatically generated file from a JSON schema."""

from typing import TypedDict, Union

JSONSchemaD2020 = Union["JSONSchemaItemD2020", bool]
""" Core vocabulary meta-schema. """


JSONSchemaItemD2020 = TypedDict(
    "JSONSchemaItemD2020",
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
        "$vocabulary": dict[str, bool],
        "$comment": str,
        "$defs": dict[str, "JSONSchemaD2020"],
    },
    total=False,
)


_AnchorString = str
""" pattern: ^[A-Za-z_][-A-Za-z0-9._]*$ """


_UriReferenceString = str
""" format: uri-reference """


_UriString = str
""" format: uri """
