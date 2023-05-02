"""
The API version draft 2019 09.
"""

import re
from typing import Any, List, Union, cast

from jsonschema_gentypes import (
    Type,
    jsonschema_draft_04,
    jsonschema_draft_2019_09_core,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
)
from jsonschema_gentypes.api_draft_07 import APIv7


class APIv201909(APIv7):
    """
    JSON Schema draft 2019 09.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.is_recursive_anchor_path: List[bool] = []
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
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proxy: Type,
        proposed_name: str,
    ) -> None:
        """
        Get the type for a schema.
        """

        schema_core = cast(jsonschema_draft_2019_09_core.JSONSchemaItemD2019, schema)

        self.is_recursive_anchor_path.append(schema_core.get("$recursiveAnchor", False))
        if self.is_recursive_anchor_path[-1]:
            del schema_core["$recursiveAnchor"]
            self.recursive_anchor_path.append(proxy)

        super().get_type_start(schema, proxy, proposed_name)

    def get_type_end(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proxy: Type,
    ) -> None:
        """
        End getting the type for a schema.
        """

        super().get_type_end(schema, proxy)

        if self.is_recursive_anchor_path[-1]:
            self.recursive_anchor_path.pop()
        self.is_recursive_anchor_path.pop()

    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """
        Handle a `$ref`.
        """

        schema_core = cast(jsonschema_draft_2019_09_core.JSONSchemaItemD2019, schema)

        if schema_core.get("$recursiveRef") == "#":
            del schema_core["$recursiveRef"]
            return self.recursive_anchor_path[-1]

        return super().ref(schema, proposed_name)
