"""
The API version draft 06.
"""

from typing import Union, cast

from jsonschema_gentypes import (
    LiteralType,
    Type,
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_2019_09,
)
from jsonschema_gentypes.api_draft_04 import APIv4


class APIv6(APIv4):
    """
    JSON Schema draft 6.
    """

    def const(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09.JSONSchemaItemD2019],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``Literal`` for a const value.
        """

        schema_casted = cast(
            Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2019_09.JSONSchemaItemD2019],
            schema,
        )

        const_: Union[int, float, str, bool, None] = schema_casted["const"]
        return LiteralType(const_)
