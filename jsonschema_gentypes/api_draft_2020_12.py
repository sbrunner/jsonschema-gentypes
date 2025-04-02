"""The API version draft 2020 12."""

from typing import Any, Union, cast

from jsonschema_gentypes import (
    BuiltinType,
    ListType,
    TupleType,
    Type,
    jsonschema_draft_04,
    jsonschema_draft_2019_09_applicator,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
)
from jsonschema_gentypes.api_draft_2019_09 import APIv201909


class APIv202012(APIv201909):
    """JSON Schema draft 2020 12."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.dynamic_anchor_type: dict[str, Type] = {}
        self.dynamic_anchor_schema: dict[
            str,
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020],
        ] = {}

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
            proxy: The proxy type for late resolving.
            proposed_name: The proposed name of the type.
        """
        schema_core = cast("jsonschema_draft_2020_12_core.JSONSchemaItemD2020", schema)

        if "$dynamicAnchor" in schema_core:
            self.dynamic_anchor_type[schema_core["$dynamicAnchor"]] = proxy
            self.dynamic_anchor_schema[schema_core["$dynamicAnchor"]] = schema
            schema.setdefault("used", set()).add("$dynamicAnchor")  # type: ignore[typeddict-item]

        super().get_type_start(schema, proxy, proposed_name)

    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """
        Handle the `$dynamicRef`.

        Parameter:
            schema: The schema to get the type for.
            proposed_name: The proposed name of the type.
        """
        schema_core = cast("jsonschema_draft_2020_12_core.JSONSchemaItemD2020", schema)

        if "$dynamicRef" in schema_core:
            dynamic_ref = schema_core["$dynamicRef"]
            schema.setdefault("used", set()).add("$dynamicRef")  # type: ignore[typeddict-item]
            return self.dynamic_anchor_type[dynamic_ref[1:]]  # Remove the starting '#' character

        return super().ref(schema, proposed_name)

    def resolve_ref(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """
        Handle the `$dynamicRef`.

        Parameter:
            schema: The schema to resolve the reference.
        """
        schema_core = cast("jsonschema_draft_2020_12_core.JSONSchemaItemD2020", schema)

        if "$dynamicRef" in schema_core:
            dynamic_ref = schema_core["$dynamicRef"]
            return self.dynamic_anchor_schema[dynamic_ref[1:]]  # Remove the starting '#' character

        return super().resolve_ref(schema)

    def array(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_applicator.JSONSchemaItemD2019,
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``List[]`` annotation with the allowed types.

        Parameter:
            schema: The schema to generate the type from.
            proposed_name: The proposed name of the type.
        """
        schema_casted = cast("jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020", schema)

        prefix_items = schema_casted.get("prefixItems")
        items = schema_casted.get("items")
        all_items: list[jsonschema_draft_2020_12_applicator.JSONSchemaD2020] = (
            prefix_items if prefix_items is not None else []
        )
        if items is not None:
            all_items = [*all_items, items]
        if prefix_items is not None:
            schema.setdefault("used", set()).add("prefixItems")  # type: ignore[typeddict-item]
            inner_types = [
                self.get_type(
                    cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                        item,
                    ),
                    f"{proposed_name} {nb}",
                )
                for nb, item in enumerate(all_items)
            ]
            type_: Type = TupleType(inner_types)
            if {schema.get("minItems"), schema.get("maxItems")} - {None, len(prefix_items)}:
                type_.set_comments(
                    [
                        "WARNING: 'prefixItems': If list, must have minItems == maxItems.",
                        "See: https://json-schema.org/understanding-json-schema/"
                        "reference/array.html#tuple-validation",
                    ],
                )
            return type_
        if items is not None:
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            return ListType(
                self.get_type(
                    cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                        items,
                    ),
                    proposed_name + " item",
                ),
            )
        type_ = BuiltinType("None")
        type_.set_comments(["WARNING: we get an array without any items"])
        return type_
