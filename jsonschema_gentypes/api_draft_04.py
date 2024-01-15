"""
The API version draft 04.
"""

import re
from typing import Any, Union, cast

from jsonschema_gentypes import (
    BuiltinType,
    CombinedType,
    NativeType,
    Type,
    TypedDictType,
    TypeEnum,
    configuration,
    get_description,
    get_name,
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_2019_09_applicator,
    jsonschema_draft_2019_09_meta_data,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
    jsonschema_draft_2020_12_validation,
)
from jsonschema_gentypes.api import API


class APIv4(API):
    """
    JSON Schema draft 4.
    """

    def enum(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate an enum.
        """
        schema.setdefault("used", set()).add("enum")  # type: ignore[typeddict-item]

        schema_meta_data = cast(
            Union[
                jsonschema_draft_04.JSONSchemaD4,
                jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
            ],
            schema,
        )

        return TypeEnum(
            get_name(schema_meta_data, proposed_name),
            cast(list[Union[int, float, bool, str, None]], schema["enum"]),
            get_description(schema_meta_data),
        )

    def boolean(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``bool`` annotation for a boolean object.
        """
        del schema, proposed_name
        return BuiltinType("bool")

    def object(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate an annotation for an object, usually a TypedDict.
        """

        schema_meta_data = cast(
            Union[
                jsonschema_draft_04.JSONSchemaD4,
                jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
            ],
            schema,
        )
        schema_validation = cast(
            Union[
                jsonschema_draft_04.JSONSchemaD4,
                jsonschema_draft_2020_12_validation.JSONSchemaItemD2020,
            ],
            schema,
        )

        std_dict = None
        name = get_name(schema_meta_data, proposed_name)
        schema.setdefault("used", set()).add("additionalProperties")  # type: ignore[typeddict-item]
        additional_properties = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
            schema.get("additionalProperties"),
        )
        if (
            additional_properties is True
            and self.additional_properties == configuration.ADDITIONALPROPERTIES_ALWAYS
        ):
            std_dict = CombinedType(NativeType("Dict"), [BuiltinType("str"), NativeType("Any")])
        elif isinstance(additional_properties, dict):
            sub_type = self.get_type(additional_properties, f"{proposed_name} additionalProperties")
            std_dict = CombinedType(NativeType("Dict"), [BuiltinType("str"), sub_type])
        else:
            pattern_properties = cast(
                dict[
                    str,
                    Union[
                        jsonschema_draft_04.JSONSchemaD4,
                        jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                    ],
                ],
                schema.get("patternProperties"),
            )
            if pattern_properties and len(pattern_properties) == 1:
                schema.setdefault("used", set()).add("patternProperties")  # type: ignore[typeddict-item]
                pattern_prop = list(pattern_properties.values())[0]
                sub_type = self.get_type(pattern_prop, f"{proposed_name} Type")
                std_dict = CombinedType(NativeType("Dict"), [BuiltinType("str"), sub_type])

        schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
        properties = cast(
            dict[
                str,
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
            ],
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

            type_: Type = TypedDictType(
                name if std_dict is None else name + "Typed",
                struct,
                get_description(schema_meta_data) if std_dict is None else [],
                required=required,
            )

            comments = []

            if std_dict is not None:
                type_ = CombinedType(NativeType("Union"), [std_dict, type_])
                comments += [
                    "",
                    "WARNING: Normally the types should be a mix of each other instead of Union.",
                    "See: https://github.com/camptocamp/jsonschema-gentypes/issues/7",
                ]

            type_.set_comments(comments)
            return type_
        if std_dict is not None:
            return std_dict
        return CombinedType(NativeType("Dict"), [BuiltinType("str"), NativeType("Any")])

    def array(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_applicator.JSONSchemaItemD2019
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``List[]`` annotation with the allowed types.
        """
        items = schema.get("items")
        if items is True:
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            return CombinedType(NativeType("List"), [NativeType("Any")])
        elif items is False:
            result = NativeType("None")
            result.set_comments(["`items: false` is not supported"])
            return result
        elif isinstance(items, list):
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            schema.setdefault("used", set()).add("additionalItems")  # type: ignore[typeddict-item]
            additional_items = schema.get("additionalItems")
            if additional_items:
                items = [*items, additional_items]
            inner_types = [
                self.get_type(
                    cast(
                        Union[
                            jsonschema_draft_04.JSONSchemaD4,
                            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                        ],
                        item,
                    ),
                    f"{proposed_name} {nb}",
                )
                for nb, item in enumerate(items)
            ]
            type_: Type = CombinedType(NativeType("Tuple"), inner_types)
            if {schema.get("minItems"), schema.get("maxItems")} - {None, len(items)}:
                type_.set_comments(
                    [
                        "WARNING: 'items': If list, must have minItems == maxItems.",
                        "See: https://json-schema.org/understanding-json-schema/"
                        "reference/array.html#tuple-validation",
                    ]
                )
            return type_
        elif items is not None:
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            return CombinedType(
                NativeType("List"),
                [
                    self.get_type(
                        cast(
                            Union[
                                jsonschema_draft_04.JSONSchemaD4,
                                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                            ],
                            items,
                        ),
                        proposed_name + " item",
                    )
                ],
            )
        else:
            schema.setdefault("used", set()).add("items")  # type: ignore[typeddict-item]
            return CombinedType(NativeType("List"), [NativeType("Any")])

    def any_of(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        sub_schema: list[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ],
        proposed_name: str,
        sub_name: str,
    ) -> Type:
        """
        Generate a ``Union`` annotation with the allowed types.
        """
        del schema

        inner_types = list(
            filter(
                lambda o: o is not None,
                [
                    self.get_type(subs, f"{proposed_name} {sub_name}{index}")
                    for index, subs in enumerate(sub_schema)
                ],
            )
        )
        return CombinedType(NativeType("Union"), inner_types)

    def all_of(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        sub_schema: list[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ],
        proposed_name: str,
        sub_name: str,
    ) -> Type:
        """
        Combine all the definitions.
        """

        all_schema: dict[str, Any] = {}
        for prop in ["title", "description", "default", "example"]:
            if prop in schema:
                all_schema[prop] = schema[prop]  # type: ignore[literal-required]

        for new_schema in sub_schema:
            new_schema = self.resolve_ref(new_schema)

            all_schema_validation = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4,
                    jsonschema_draft_2020_12_validation.JSONSchemaItemD2020,
                ],
                all_schema,
            )
            new_schema_validation = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4,
                    jsonschema_draft_2020_12_validation.JSONSchemaItemD2020,
                ],
                new_schema,
            )

            combined_schema: dict[str, Any] = {}
            if "properties" in new_schema and "properties" in all_schema:
                all_schema.setdefault("used", set()).add("properties")
                new_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
                combined_schema["properties"] = {
                    **all_schema["properties"],
                    **new_schema["properties"],
                }
            if "required" in new_schema and "required" in all_schema:
                combined_schema["required"] = list(
                    {
                        *all_schema_validation["required"],
                        *new_schema_validation["required"],
                    }
                )
            if "type" in new_schema and "type" in all_schema:
                all_type = (
                    all_schema_validation["type"]
                    if isinstance(all_schema_validation["type"], list)
                    else [all_schema_validation["type"]]
                )
                new_type = (
                    new_schema_validation["type"]
                    if isinstance(new_schema_validation["type"], list)
                    else [new_schema_validation["type"]]
                )
                combined_schema["type"] = [t for t in all_type if t in new_type]

            all_schema.update(new_schema)
            all_schema.update(combined_schema)

        return self.get_type(
            cast(
                Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
                all_schema,
            ),
            proposed_name,
        )

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
        else:
            if re.search("[a-z]", ref_proposed_name):
                ref_proposed_name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", ref_proposed_name).lower()
        return ref_proposed_name

    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """
        Handle a `$ref`.
        """

        # ref is not correctly declared in draft 4.
        schema_casted = cast(
            Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
            schema,
        )

        ref = schema_casted["$ref"]
        schema.setdefault("used", set()).add("$ref")  # type: ignore[typeddict-item]

        if ref == "#":  # Self ref.
            # Per @ilevkivskyi:
            #
            # > You should never use ForwardRef manually
            # > Also it is deprecated and will be removed soon
            # > Support for recursive types is limited to proper classes
            # > currently
            #
            # forward_ref = ForwardRef(UnboundType(self.outer_name))
            # self.forward_refs.append(forward_ref)
            # return forward_ref

            assert self.root is not None
            return self.root

        if ref in self.ref_type:
            return self.ref_type[ref]

        resolved = self.resolver.lookup(ref)

        type_ = self.get_type(
            cast(
                Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
                resolved,
            ),
            self.ref_to_proposed_name(ref),
        )
        self.ref_type[ref] = type_
        return type_

    def string(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``str`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("str")

    def number(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate a ``Union[int, float]`` annotation.
        """
        del schema, proposed_name
        return CombinedType(NativeType("Union"), [BuiltinType("int"), BuiltinType("float")])

    def integer(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate an ``int`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("int")

    def null(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Generate an ``None`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("None")

    def default(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019
        ],
        proposed_name: str,
    ) -> Type:
        """
        Treat the default keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """

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
