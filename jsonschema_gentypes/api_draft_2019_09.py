"""
The API version draft 2019 09.
"""

import re
from typing import Any, List, Union, cast

from jsonschema_gentypes import (
    Type,
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_07,
    jsonschema_draft_2019_09,
)
from jsonschema_gentypes.api_draft_07 import APIv7


class APIv201909(APIv7):
    """
    JSON Schema draft 2019 09.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.recursive_anchor_path: List[Type] = []

    def ref_to_proposed_name(self, ref: str) -> str:
        """
        Create a proposed name from a ref.

        Change the case from camel case to standard case, this is for layer inverse conversion then don't lost the case.
        """
        ref_proposed_name = ref
        if ref.startswith("#/$defs/"):
            ref_proposed_name = ref[len("#/$defs/") :]
        elif ref.startswith("#/"):
            ref_proposed_name = ref[len("#/") :]
        if "/" in ref_proposed_name:
            ref_proposed_name = ref_proposed_name.replace("/", " ")
        else:
            if re.search("[a-z]", ref_proposed_name):
                ref_proposed_name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", ref_proposed_name).lower()
        return ref_proposed_name

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_06.JSONSchemaItemD6,
            jsonschema_draft_07.JSONSchemaItemD7,
            jsonschema_draft_2019_09.JSONSchemaItemD2019,
        ],
        proxy: Type,
    ) -> None:
        """
        Get the type for a schema.
        """
        if schema.get("$recursiveAnchor", False):
            self.recursive_anchor_path.append(proxy)

    def get_type_end(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_06.JSONSchemaItemD6,
            jsonschema_draft_07.JSONSchemaItemD7,
            jsonschema_draft_2019_09.JSONSchemaItemD2019,
        ],
        proxy: Type,
    ) -> None:
        """
        End getting the type for a schema.
        """
        if schema.get("$recursiveAnchor", False):
            self.recursive_anchor_path.pop()

    def ref(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_06.JSONSchemaItemD6,
            jsonschema_draft_07.JSONSchemaItemD7,
            jsonschema_draft_2019_09.JSONSchemaItemD2019,
        ],
        proposed_name: str,
    ) -> Type:
        """
        Handle a `$ref`.
        """

        schema_2019 = cast(Union[jsonschema_draft_2019_09.JSONSchemaItemD2019], schema)
        if schema_2019.get("$recursiveRef") == "#":
            del schema_2019["$recursiveRef"]  # type: ignore
            return self.recursive_anchor_path[-1]

        return super().ref(schema, proposed_name)