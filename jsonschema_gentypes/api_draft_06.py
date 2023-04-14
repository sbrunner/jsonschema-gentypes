"""
The API version draft 06.
"""

from typing import Union, cast

from jsonschema_gentypes import (
    LiteralType,
    Type,
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_validation,
)
from jsonschema_gentypes.api_draft_04 import APIv4


class APIv6(APIv4):
    """
    JSON Schema draft 6.
    """

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proxy: Type,
    ) -> None:
        """
        Get the type for a schema.
        """

        schema_casted = cast(
            Union[
                jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
            ],
            schema,
        )
        property_names = schema_casted.get("propertyNames")
        if isinstance(property_names, dict) and "type" in property_names:
            property_names["__type__"] = property_names["type"]  # type: ignore
            del property_names["type"]  # type: ignore

        super().get_type_start(schema, proxy)

    def const(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``Literal`` for a const value.
        """

        schema_casted = cast(
            Union[
                jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020
            ],
            schema,
        )

        const_: Union[int, float, str, bool, None] = schema_casted["const"]
        return LiteralType(const_)
