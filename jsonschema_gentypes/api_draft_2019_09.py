"""The API version draft 2019 09."""

import re
from typing import TYPE_CHECKING, Any, Union, cast

from jsonschema_gentypes import (
    Type,
    jsonschema_draft_04,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
)
from jsonschema_gentypes.api_draft_07 import APIv7

if TYPE_CHECKING:
    from jsonschema_gentypes import (
        jsonschema_draft_2019_09_core,
    )


class APIv201909(APIv7):
    """JSON Schema draft 2019 09."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.is_recursive_anchor_path: list[bool] = []
        self.recursive_anchor_path_type: list[Type] = []
        self.recursive_anchor_path_schema: list[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ] = []

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
        elif re.search("[a-z]", ref_proposed_name):
            ref_proposed_name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", ref_proposed_name).lower()
        return ref_proposed_name

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proxy: Type,
        proposed_name: str,
    ) -> None:
        """
        Get the type for a schema.

        Parameter:
            schema: The schema to get the type for.
            proxy: The proxy used for late resolving.
            proposed_name: The proposed name of the type.
        """
        schema_core = cast("jsonschema_draft_2019_09_core.JSONSchemaItemD2019", schema)

        self.is_recursive_anchor_path.append(schema_core.get("$recursiveAnchor", False))
        if self.is_recursive_anchor_path[-1]:
            schema.setdefault("used", set()).add("$recursiveAnchor")  # type: ignore[typeddict-item]
            self.recursive_anchor_path_type.append(proxy)
            self.recursive_anchor_path_schema.append(schema)

        super().get_type_start(schema, proxy, proposed_name)

    def get_type_end(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proxy: Type,
    ) -> None:
        """
        End getting the type for a schema.

        Parameter:
            schema: The schema to get the type for.
            proxy: The proxy to get the type for.
        """
        super().get_type_end(schema, proxy)

        if self.is_recursive_anchor_path[-1]:
            self.recursive_anchor_path_type.pop()
            self.recursive_anchor_path_schema.pop()
        self.is_recursive_anchor_path.pop()

    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """
        Handle the `$recursiveRef`.

        Parameter:
            schema: The schema to get the type for.
        """
        schema_core = cast("jsonschema_draft_2019_09_core.JSONSchemaItemD2019", schema)

        if schema_core.get("$recursiveRef") == "#":
            schema.setdefault("used", set()).add("$recursiveRef")  # type: ignore[typeddict-item]
            return self.recursive_anchor_path_type[-1]

        return super().ref(schema, proposed_name)

    def resolve_ref(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """
        Handle the `$recursiveRef`.

        Parameter:
            schema: The schema to resolve.
        """
        schema_core = cast("jsonschema_draft_2020_12_core.JSONSchemaItemD2020", schema)

        if schema_core.get("$recursiveRef") == "#":
            return self.recursive_anchor_path_schema[-1]

        return super().resolve_ref(schema)
