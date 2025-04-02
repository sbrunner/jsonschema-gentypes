"""The API version draft 06."""

from typing import TYPE_CHECKING, Any, Union, cast

from jsonschema_gentypes import (
    LiteralType,
    Type,
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_2020_12_applicator,
)
from jsonschema_gentypes.api_draft_04 import APIv4

if TYPE_CHECKING:
    from jsonschema_gentypes import (
        jsonschema_draft_2020_12_validation,
    )


class APIv6(APIv4):
    """JSON Schema draft 6."""

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proxy: Type,
        proposed_name: str,
    ) -> None:
        """Get the type for a schema."""
        schema_casted = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
            schema,
        )
        property_names = schema_casted.get("propertyNames")
        if isinstance(property_names, dict) and "type" in property_names:
            property_names["__type__"] = property_names["type"]  # type: ignore[typeddict-unknown-key,typeddict-item]
            del property_names["type"]  # type: ignore[typeddict-item]

        super().get_type_start(schema, proxy, proposed_name)

    def build_type(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """
        Build a type for a schema.

        Parameter:
            schema: The schema to get the type for.
            proposed_name: The proposed name of the type.
        """
        if "const" in schema:
            return self.const(
                cast(
                    "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                    schema,
                ),
            )

        return super().build_type(schema, proposed_name)

    def const(
        self,
        schema: Union[
            jsonschema_draft_06.JSONSchemaItemD6,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Type:
        """
        Treat the const  keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html#constant-values

        Generate a ``Literal`` for a const value.

        Parameter:
            schema: The schema to get the type for.
        """
        schema_casted = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            schema,
        )

        schema.setdefault("used", set()).add("const")  # type: ignore[typeddict-item]
        const_: Union[int, float, str, bool, None, dict[str, Any], list[Any]] = schema_casted["const"]
        return LiteralType(const_)
