"""
The API base definition.
"""

from abc import abstractmethod
from typing import Callable, Dict, List, Optional, Union, cast

from jsonschema_gentypes import (
    BuiltinType,
    CombinedType,
    Constant,
    NamedType,
    NativeType,
    Type,
    TypeAlias,
    TypeProxy,
    configuration,
    get_description,
    get_name,
    jsonschema_draft_04,
    jsonschema_draft_2019_09_meta_data,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
    jsonschema_draft_2020_12_validation,
)
from jsonschema_gentypes.resolver import RefResolver

# Raise issues here.
ISSUE_URL = "https://github.com/camptcamp/jsonschema-gentypes"


class API:
    r"""
    Base class for JSON schema types API.

    Call tree:
      get_type()
        |-> get_type_start()
        |-> build_type()
        |     |-> _resolve_ref()
        |     |-> get_type()
        |     |-> ref()
        |     |-> any_of()
        |     |-> enum()
        |     |-> default()
        |     \-> _get_type()
        |           \-> get_type_handler()
        \-> get_type_end()
    """

    def __init__(
        self,
        resolver: RefResolver,
        additional_properties: configuration.AdditionalProperties = configuration.ADDITIONALPROPERTIES_ONLY_EXPLICIT,
    ) -> None:
        """
        Initialize with a resolver.
        """
        self.resolver = resolver
        self.additional_properties = additional_properties
        # types by reference
        self.ref_type: Dict[str, Type] = {}
        self.root: Optional[TypeProxy] = None

    def get_type_handler(
        self, schema_type: str
    ) -> Callable[
        [
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020],
            str,
        ],
        Type,
    ]:
        """
        Get a handler from this schema draft version.
        """
        if schema_type.startswith("_"):
            raise AttributeError("No way friend")
        handler = cast(
            Callable[
                [
                    Union[
                        jsonschema_draft_04.JSONSchemaD4,
                        jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                    ],
                    str,
                ],
                Type,
            ],
            getattr(self, schema_type, None),
        )
        if handler is None:
            raise NotImplementedError(
                f"Type `{schema_type}` is not supported. If you think that this is an error, "
                f"say something at {ISSUE_URL}"
            )
        return handler

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proxy: Type,
        proposed_name: str,
    ) -> None:
        """
        Start getting the type for a schema.
        """

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

    def get_type(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
        proposed_name: str,
        auto_alias: bool = True,
    ) -> Type:
        """
        Get a :class:`.Type` for a JSON schema.
        """

        schema_meta_data = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019],
            schema,
        )

        root = self.root is None
        if root:
            self.root = TypeProxy()
        if schema is True:
            type_ = NativeType("Any")
            if root:
                assert self.root is not None
                self.root.set_type(type_)
            return type_
        if schema is False:
            type_ = NativeType("None")
            if root:
                assert self.root is not None
                self.root.set_type(type_)
            return type_
        assert not isinstance(schema, bool)

        proxy = TypeProxy()

        self.get_type_start(schema, proxy, proposed_name)

        the_type = self.build_type(schema, proposed_name)
        assert the_type is not None
        additional_description = the_type.comments()
        description = get_description(schema_meta_data)
        if description and additional_description:
            description.append("")
        description += additional_description
        if not isinstance(the_type, NamedType) and description:
            if auto_alias:
                the_type = TypeAlias(get_name(schema_meta_data, proposed_name), the_type, description)
            else:
                the_type.set_comments(description)

        if "default" in schema_meta_data:
            the_type.add_depends_on(
                Constant(
                    f"{get_name(schema_meta_data, proposed_name, True)}_DEFAULT",
                    schema_meta_data["default"],
                    [f"Default value of the field path '{proposed_name}'"],
                )
            )

        proxy.set_type(the_type)
        if root:
            assert self.root is not None
            self.root.set_type(the_type)

        self.get_type_end(schema, proxy)

        return the_type

    def _resolve_ref(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        if "$ref" in schema:
            with self.resolver.resolving(schema["$ref"]) as resolved:  # type: ignore
                schema.update(resolved)
        return schema

    def build_type(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """Get a :class:`.Type` for a JSON schema."""

        schema_meta_data = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019],
            schema,
        )
        schema_core = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
            schema,
        )

        proposed_name = schema_meta_data.get("title", proposed_name)

        if "if" in schema:
            base_schema = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                {},
            )
            base_schema.update(schema)  # type: ignore
            for key in ("if", "then", "else", "title", "description"):
                if key in base_schema:
                    del base_schema[key]  # type: ignore
            then_schema = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                {},
            )
            then_schema.update(base_schema)  # type: ignore
            then_schema.update(
                self._resolve_ref(  # type: ignore
                    cast(
                        Union[
                            jsonschema_draft_04.JSONSchemaD4,
                            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                        ],
                        schema.get("then", {}),
                    )
                )
            )
            if "properties" not in then_schema:
                then_schema["properties"] = {}
            then_properties = then_schema["properties"]
            assert then_properties
            if_properties = self._resolve_ref(
                cast(
                    Union[
                        jsonschema_draft_04.JSONSchemaD4,
                        jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                    ],
                    schema.get("if", {}),
                )
            ).get("properties", {})
            assert if_properties
            then_properties.update(if_properties)  # type: ignore
            else_schema = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                {},
            )
            else_schema.update(base_schema)  # type: ignore
            else_schema.update(
                self._resolve_ref(  # type: ignore
                    cast(
                        Union[
                            jsonschema_draft_04.JSONSchemaD4,
                            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                        ],
                        schema.get("else", {}),
                    )
                )
            )

            return CombinedType(
                NativeType("Union"),
                [
                    self.get_type(then_schema, proposed_name + " then"),
                    self.get_type(else_schema, proposed_name + " else"),
                ],
            )

        if "$ref" in schema or "$recursiveRef" in schema or "$dynamicRef" in schema:
            return self.ref(schema_core, proposed_name)

        schema_meta_data = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019],
            schema,
        )
        schema_validation = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020],
            schema,
        )

        # 6.1.1. type
        # The value of this keyword MUST be either a string or an array. If it
        # is an array, elements of the array MUST be strings and MUST be
        # unique.
        #
        # String values MUST be one of the six primitive types ("null",
        # "boolean", "object", "array", "number", or "string"), or "integer"
        # which matches any number with a zero fractional part.
        #
        # An instance validates if and only if the instance is in any of the
        # sets listed for this keyword.
        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            inner_types = []
            proposed_name = schema_meta_data.get("title", proposed_name)
            schema_copy = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                dict(schema),
            )
            schema_meta_data_copy = cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019
                ],
                schema_copy,
            )

            if "title" in schema_meta_data_copy:
                del schema_meta_data_copy["title"]
            for primitive_type in schema_type:
                inner_types.append(
                    self._get_type(
                        schema_copy, cast(str, primitive_type), f"{proposed_name} {primitive_type}"
                    )
                )
            return CombinedType(NativeType("Union"), inner_types)
        elif schema_type is None:
            if "allOf" in schema:
                type_ = self.any_of(
                    schema,
                    cast(
                        List[
                            Union[
                                jsonschema_draft_04.JSONSchemaD4,
                                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                            ]
                        ],
                        schema["allOf"],
                    ),
                    proposed_name,
                    "allof",
                )
                if type_.comments():
                    type_.comments().append("")
                type_.comments().append("WARNING: PEP 544 does not support an Intersection type,")
                type_.comments().append("so `allOf` is interpreted as a `Union` for now.")
                type_.comments().append("See: https://github.com/camptocamp/jsonschema-gentypes/issues/8")
                return type_
            elif "anyOf" in schema:
                return self.any_of(
                    schema,
                    cast(
                        List[
                            Union[
                                jsonschema_draft_04.JSONSchemaD4,
                                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                            ]
                        ],
                        schema["anyOf"],
                    ),
                    proposed_name,
                    "anyof",
                )
            elif "oneOf" in schema:
                type_ = self.any_of(
                    schema,
                    cast(
                        List[
                            Union[
                                jsonschema_draft_04.JSONSchemaD4,
                                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                            ]
                        ],
                        schema["oneOf"],
                    ),
                    proposed_name,
                    "oneof",
                )
                if type_.comments():
                    type_.comments().append("")
                type_.comments().append("oneOf")
                return type_
            elif "enum" in schema:
                return self.enum(schema_validation, proposed_name)
            elif "default" in schema:
                return self.default(schema_meta_data, proposed_name)

        if schema_type is None:
            type_ = BuiltinType("Any")
            type_.set_comments(["WARNING: we get an schema without any type"])
            return type_
        assert isinstance(schema_type, str), (
            f"Expected to find a supported schema type, got {schema_type}" f"\nDuring parsing of {schema}"
        )

        return self._get_type(schema, schema_type, proposed_name)

    def _get_type(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        schema_type: str,
        proposed_name: str,
    ) -> Type:
        schema_meta_data = cast(
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019],
            schema,
        )

        proposed_name = schema_meta_data.get("title", proposed_name)

        # Enums get special treatment, as they should be one of the literal values.
        # Note: If a "type" field indicates types that are incompatible with some of
        # the enumeration values (which is allowed by jsonschema), the "type" will _not_
        # be respected. This should be considered a malformed schema anyway, so this
        # will not be fixed.
        if "enum" in schema:
            handler = self.get_type_handler("enum")
            return handler(schema, proposed_name)

        handler = self.get_type_handler(schema_type)
        if handler is not None:
            return handler(schema, proposed_name)

        type_ = BuiltinType("None")
        type_.set_comments(
            [
                f"WARNING: No handler for `{schema_type}`; please raise an issue",
                f"at {ISSUE_URL} if you believe this to be in error",
            ]
        )
        return type_

    @abstractmethod
    def ref(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020],
        proposed_name: str,
    ) -> Type:
        """
        Treat the ref keyword.

        See: https://json-schema.org/understanding-json-schema/structuring.html#ref.
        """

    @abstractmethod
    def any_of(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
        ],
        sub_schema: List[
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]
        ],
        proposed_name: str,
        sub_name: str,
    ) -> Type:
        """
        Treat the anyOf keyword.

        See: https://json-schema.org/understanding-json-schema/reference/combining.html#anyof.
        """

    @abstractmethod
    def enum(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020
        ],
        proposed_name: str,
    ) -> Type:
        """
        Treat enum.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html#enumerated-values
        """

    @abstractmethod
    def default(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019
        ],
        proposed_name: str,
    ) -> Type:
        """
        Treat the default  keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """
