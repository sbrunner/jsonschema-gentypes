"""The API version draft 04."""

import re
from typing import TYPE_CHECKING, Literal, Union, cast

from jsonschema_gentypes import (
    BuiltinType,
    DictType,
    ListType,
    NamedType,
    NativeType,
    TupleType,
    Type,
    TypeAlias,
    TypedDictType,
    TypeEnum,
    TypeProxy,
    UnionType,
    configuration,
    get_description,
    jsonschema_draft_04,
    jsonschema_draft_2019_09_applicator,
    jsonschema_draft_2019_09_meta_data,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
    jsonschema_draft_2020_12_validation,
)
from jsonschema_gentypes.api import API

if TYPE_CHECKING:
    from jsonschema_gentypes import (
        jsonschema_draft_06,
    )


class APIv4(API):
    """JSON Schema draft 4."""

    def enum(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_validation.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate an enum."""
        schema.setdefault("used", set()).add("enum")  # type: ignore[typeddict-item]

        schema_meta_data = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
            schema,
        )

        return TypeEnum(
            self.get_name(schema_meta_data, proposed_name),
            cast("list[Union[int, float, bool, str, None]]", schema["enum"]),
            get_description(schema_meta_data),
        )

    def boolean(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate a ``bool`` annotation for a boolean object."""
        del schema, proposed_name
        return BuiltinType("bool")

    def object(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate an annotation for an object, usually a TypedDict."""
        schema_meta_data = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
            schema,
        )
        schema_validation = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            schema,
        )

        std_dict = None

        schema.setdefault("used", set()).add("additionalProperties")  # type: ignore[typeddict-item]
        additional_properties = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020]",
            schema.get("additionalProperties"),
        )
        if (
            additional_properties is True
            and self.additional_properties == configuration.ADDITIONALPROPERTIES_ALWAYS
        ):
            std_dict = DictType(BuiltinType("str"), NativeType("Any"))
        elif isinstance(additional_properties, dict):
            sub_type = self.get_type(additional_properties, f"{proposed_name} additionalProperties")
            std_dict = DictType(BuiltinType("str"), sub_type)
        else:
            pattern_properties = cast(
                "dict[str, Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]]",
                schema.get("patternProperties"),
            )
            if pattern_properties and len(pattern_properties) == 1:
                schema.setdefault("used", set()).add("patternProperties")  # type: ignore[typeddict-item]
                pattern_prop = next(iter(pattern_properties.values()))
                sub_type = self.get_type(pattern_prop, f"{proposed_name} Type")
                std_dict = DictType(BuiltinType("str"), sub_type)

        schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
        properties = cast(
            "dict[str, Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]]",
            schema.get("properties"),
        )
        proposed_name = schema_meta_data.get("title", proposed_name)
        if properties:
            required = set(schema_validation.get("required", []))
            schema.setdefault("used", set()).add("required")  # type: ignore[typeddict-item]

            struct = {
                prop: self.get_type(sub_schema, proposed_name + " " + prop, auto_alias=False)
                for prop, sub_schema in properties.items()
            }

            name = self.get_name(
                schema_meta_data,
                proposed_name,
                postfix="Typed" if std_dict is not None else "",
            )
            type_: Type = TypedDictType(
                name,
                struct,
                get_description(schema_meta_data) if std_dict is None else [],
                required=required,
            )

            comments = []

            if std_dict is not None:
                type_ = UnionType([std_dict, type_])
                comments += [
                    "",
                    "WARNING: Normally the types should be a mix of each other instead of Union.",
                    "See: https://github.com/camptocamp/jsonschema-gentypes/issues/7",
                ]

            type_.set_comments(comments)
            return type_
        if std_dict is not None:
            return std_dict
        return DictType(BuiltinType("str"), NativeType("Any"))

    def array(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_applicator.JSONSchemaItemD2019,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate a ``List[]`` annotation with the allowed types."""
        items = schema.get("items")
        if items is True:
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            return ListType(NativeType("Any"))
        if items is False:
            result = NativeType("None")
            result.set_comments(["`items: false` is not supported"])
            return result
        if isinstance(items, list):
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            schema.setdefault("used", set()).add("additionalItems")  # type: ignore[typeddict-item]
            additional_items = schema.get("additionalItems")
            if additional_items:
                items = [*items, additional_items]
            inner_types = [
                self.get_type(
                    cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                        item,
                    ),
                    f"{proposed_name} {nb}",
                )
                for nb, item in enumerate(items)
            ]
            type_: Type = TupleType(inner_types)
            if {schema.get("minItems"), schema.get("maxItems")} - {None, len(items)}:
                type_.set_comments(
                    [
                        "WARNING: 'items': If list, must have minItems == maxItems.",
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
        schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
        return ListType(NativeType("Any"))

    def any_of(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        sub_schemas: Union[
            list[jsonschema_draft_04.JSONSchemaD4],
            list[jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
        ],
        proposed_name: str,
        sub_name: str,
        recursion: int = 0,
    ) -> tuple[
        Type,
        list[Type],
        list[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ],
    ]:
        """Generate a ``Union`` annotation with the allowed types."""
        if recursion > 10:
            message = "Recursion limit reached"
            raise ValueError(message)

        additional_types: list[Type] = []
        inner_types: list[Type] = []
        inner_types_schema: list[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ] = []

        for index, sub_schema in enumerate(sub_schemas):
            assert not isinstance(sub_schema, bool)
            sub_schema = self.combined_sub_type(schema, sub_schema)  # noqa: PLW2901
            force_sub_type = "title" in sub_schema
            if "allOf" in sub_schema:
                type_, named_types, combined_schema = self.all_of(
                    sub_schema,
                    sub_schema["allOf"],
                    proposed_name + " " + sub_name,
                    "allof",
                    recursion=recursion + 1,
                )
                additional_types += named_types
                if force_sub_type:
                    combined_schema_meta_data = cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
                        combined_schema,
                    )
                    if not isinstance(type_, NamedType):
                        type_ = TypeAlias(
                            self.get_name(combined_schema_meta_data, proposed_name + " " + sub_name),
                            type_,
                            [],
                        )

                    additional_types.append(type_)
                inner_types.append(type_)
                inner_types_schema.append(combined_schema)
            elif ("anyOf" in sub_schema and self.significative_sub_type(sub_schema["anyOf"])) or (
                "oneOf" in sub_schema and self.significative_sub_type(sub_schema["oneOf"])
            ):
                kind: Literal["anyOf", "oneOf"] = "anyOf" if "anyOf" in sub_schema else "oneOf"
                sub_schema = self.combined_sub_type(schema, sub_schema)  # noqa: PLW2901
                type_, named_types, combined_schemas = self.any_of(
                    sub_schema,
                    sub_schema[kind],
                    proposed_name + " " + sub_name,
                    kind,
                    recursion=recursion + 1,
                )
                additional_types += named_types
                if force_sub_type:
                    combined_schema_meta_data = cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
                        combined_schemas,
                    )
                    if not isinstance(type_, NamedType):
                        type_ = TypeAlias(
                            self.get_name(combined_schema_meta_data, proposed_name + " " + sub_name),
                            type_,
                            [],
                        )
                    additional_types.append(type_)
                inner_types.append(type_)
                inner_types_schema += combined_schemas
            else:
                sub_schema = self.combined_sub_type(schema, sub_schema)  # noqa: PLW2901
                inner_types_schema.append(sub_schema)
                sub_type = self.get_type(sub_schema, f"{proposed_name} {sub_name}{index}")
                if force_sub_type:
                    additional_types.append(sub_type)
                inner_types.append(sub_type)

        return UnionType(inner_types), additional_types, inner_types_schema

    def clean_schema(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """Remove the properties that could not be combined with an other type."""
        return {  # type: ignore[return-value]
            k: v
            for k, v in schema.items()
            if k not in ["title", "description", "example", "allOf", "anyOf", "oneOf"]
        }

    def combined_sub_type(
        self,
        base_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        sub_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """Create a sub schema with the elements from the base schema."""
        combined_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ] = {}
        combined_schema.update(self.clean_schema(base_schema))  # type: ignore[typeddict-item]
        combined_schema.update(sub_schema)  # type: ignore[typeddict-item]
        return combined_schema

    def combined_base_type_all_of(
        self,
        base_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        sub_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """Create a sub schema with the elements from the base schema."""
        assert not isinstance(sub_schema, bool)

        base_schema_validation = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            base_schema,
        )
        sub_schema_validation = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            sub_schema,
        )

        combined_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ] = {}
        combined_schema_validation = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            combined_schema,
        )
        combined_schema.update(base_schema)  # type: ignore[typeddict-item]
        combined_schema.update(self.clean_schema(sub_schema))  # type: ignore[typeddict-item]

        if "properties" in base_schema and "properties" in sub_schema:
            base_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
            sub_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
            combined_schema["properties"] = {
                **base_schema["properties"],  # type: ignore[dict-item]
                **sub_schema["properties"],  # type: ignore[dict-item]
            }
        if "required" in base_schema and "required" in sub_schema_validation:
            combined_schema_validation["required"] = list(
                {
                    *base_schema_validation["required"],
                    *sub_schema_validation["required"],
                },
            )
        if "type" in base_schema and "type" in sub_schema_validation:
            base_type = (
                base_schema_validation["type"]
                if isinstance(base_schema_validation["type"], list)
                else [base_schema_validation["type"]]
            )
            sub_type = (
                sub_schema_validation["type"]
                if isinstance(sub_schema_validation["type"], list)
                else [sub_schema_validation["type"]]
            )
            combined_schema_validation["type"] = [t for t in base_type if t in sub_type]
        return combined_schema

    def all_of(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        sub_schemas: Union[
            list[jsonschema_draft_04.JSONSchemaD4],
            list[jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
        ],
        proposed_name: str,
        sub_name: str,
        recursion: int = 0,
    ) -> tuple[
        Type,
        list[Type],
        Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020],
    ]:
        """Combine all the definitions."""
        if recursion > 10:
            message = "Recursion limit reached"
            raise ValueError(message)

        additional_types: list[Type] = []

        all_schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ] = {}
        all_schema.update(schema)  # type: ignore[typeddict-item]
        for prop in ["allOf", "anyOf", "oneOf"]:
            if prop in all_schema:
                del all_schema[prop]  # type: ignore[misc]

        for index, new_schema in enumerate(sub_schemas):
            assert not isinstance(new_schema, bool)
            new_schema = self.resolve_ref(new_schema)  # noqa: PLW2901
            force_sub_type = "title" in new_schema
            if "allOf" in new_schema and self.significative_sub_type(new_schema["allOf"]):
                type_, named_types, combined_schema = self.all_of(
                    self.combined_sub_type(schema, new_schema),
                    new_schema["allOf"],
                    f"{proposed_name} {sub_name}{index}",
                    "allof",
                    recursion=recursion + 1,
                )

                additional_types += named_types
                if force_sub_type:
                    combined_schema_meta_data = cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
                        combined_schema,
                    )
                    if not isinstance(type_, NamedType):
                        type_ = TypeAlias(
                            self.get_name(combined_schema_meta_data, f"{proposed_name} {sub_name}{index}"),
                            type_,
                            [],
                        )

                    additional_types.append(type_)
                all_schema = self.combined_base_type_all_of(all_schema, combined_schema)
            elif "anyOf" in new_schema or "oneOf" in new_schema:
                kind_name = "anyOf" if "anyOf" in new_schema else "oneOf"
                type_, named_types, combined_schemas = self.any_of(
                    self.combined_sub_type(schema, new_schema),
                    new_schema[kind_name],  # type: ignore[literal-required]
                    f"{proposed_name} {sub_name}{index}",
                    kind_name,
                    recursion=recursion + 1,
                )
                additional_types += named_types
                if force_sub_type:
                    combined_schema_meta_data = cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
                        combined_schemas,
                    )
                    if not isinstance(type_, NamedType):
                        type_ = TypeAlias(
                            self.get_name(combined_schema_meta_data, f"{proposed_name} {sub_name}{index}"),
                            type_,
                            [],
                        )
                    additional_types.append(type_)
                for combined_schema in combined_schemas:
                    all_schema = self.combined_base_type_all_of(all_schema, combined_schema)
            else:
                combined_schema = self.combined_sub_type(schema, new_schema)
                if force_sub_type:
                    additional_types.append(
                        self.get_type(combined_schema, f"{proposed_name} {sub_name}{index}"),
                    )
                all_schema = self.combined_base_type_all_of(all_schema, combined_schema)

        type_ = self.get_type(
            cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020]",
                all_schema,
            ),
            proposed_name,
        )

        return type_, additional_types, all_schema

    def ref_to_proposed_name(self, ref: str) -> str:
        """
        Create a proposed name from a ref.

        Change the case from camel case to standard case, this is for layer inverse conversion then don't lost the case.
        """
        ref_proposed_name = ref
        if ref.startswith("#/definitions/"):
            ref_proposed_name = ref[len("#/definitions/") :]
        elif ref.startswith("#/"):
            ref_proposed_name = ref[len("#/") :]
        if "/" in ref_proposed_name:
            ref_proposed_name = ref_proposed_name.replace("/", " ")
        elif re.search("[a-z]", ref_proposed_name):
            ref_proposed_name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", ref_proposed_name).lower()
        return ref_proposed_name

    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """Handle a `$ref`."""
        del proposed_name
        # ref is not correctly declared in draft 4.
        schema_casted = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            schema,
        )

        ref = schema_casted["$ref"]
        schema.setdefault("used", set()).add("$ref")  # type: ignore[typeddict-item]

        if ref == "#":  # Self ref.
            assert self.root is not None
            return self.root

        if ref in self.ref_type:
            return self.ref_type[ref]

        resolved = self.resolver.lookup(ref)
        proxy = TypeProxy()
        self.ref_type[ref] = proxy

        type_ = self.get_type(
            cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020]",
                resolved,
            ),
            self.ref_to_proposed_name(ref),
        )
        proxy.set_type(type_)
        self.ref_type[ref] = type_

        return type_

    def string(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate a ``str`` annotation."""
        del schema, proposed_name
        return BuiltinType("str")

    def number(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate a ``Union[int, float]`` annotation."""
        del schema, proposed_name
        return UnionType([BuiltinType("int"), BuiltinType("float")])

    def integer(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate an ``int`` annotation."""
        del schema, proposed_name
        return BuiltinType("int")

    def null(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Generate an ``None`` annotation."""
        del schema, proposed_name
        return BuiltinType("None")

    def default(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
        ],
        proposed_name: str,
    ) -> Type:
        """
        Treat the default keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """
        del proposed_name
        type_: Type = NativeType("Any")
        for test_type, type_name in [
            (str, "str"),
            (int, "int"),
            (float, "float"),
            (bool, "bool"),
        ]:
            if isinstance(schema["default"], test_type):
                type_ = BuiltinType(type_name)
        return type_
