"""The API base definition."""

from abc import abstractmethod
from typing import TYPE_CHECKING, Callable, Optional, Union, cast

from jsonschema_gentypes import (
    BuiltinType,
    CombinedType,
    Constant,
    NamedType,
    NativeType,
    Type,
    TypeAlias,
    TypeProxy,
    UnionType,
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

if TYPE_CHECKING:
    from jsonschema_gentypes import (
        jsonschema_draft_06,
    )
# Raise issues here.
ISSUE_URL = "https://github.com/camptcamp/jsonschema-gentypes"


class API:
    r"""
    Base class for JSON schema types API.

    Call tree:
      get_type()
        |-> get_type_start()
        |-> build_type()
        |     |-> resolve_ref()
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
        python_version: tuple[int, ...],
        additional_properties: configuration.AdditionalProperties = configuration.ADDITIONALPROPERTIES_ONLY_EXPLICIT,
        get_name_properties: configuration.GetNameProperties = configuration.GETNAMEPROPERTIES_TITLE,
    ) -> None:
        """Initialize with a resolver."""
        self.resolver = resolver
        self.python_version = python_version
        self.additional_properties = additional_properties
        self.get_name_properties = get_name_properties
        # types by reference
        self.ref_type: dict[str, Type] = {}
        self.root: Optional[TypeProxy] = None

    def get_type_handler(
        self,
        schema_type: str,
    ) -> Callable[
        [
            Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020],
            str,
        ],
        Type,
    ]:
        """Get a handler from this schema draft version."""
        if schema_type.startswith("_"):
            message = "No way friend"
            raise AttributeError(message)
        handler = cast(
            "Callable[[Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020], str], Type]",
            getattr(self, schema_type, None),
        )
        if handler is None:
            raise NotImplementedError(
                f"Type `{schema_type}` is not supported. If you think that this is an error, "
                f"say something at {ISSUE_URL}",
            )
        return handler

    def get_type_start(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proxy: Type,
        proposed_name: str,
    ) -> None:
        """Start getting the type for a schema."""

    def get_type_end(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proxy: Type,
    ) -> None:
        """End getting the type for a schema."""

    def get_type(
        self,
        schema: Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
        proposed_name: str,
        auto_alias: bool = True,
    ) -> Type:
        """Get a :class:`.Type` for a JSON schema."""
        schema_meta_data = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
            schema,
        )

        root = self.root is None
        if root:
            self.root = TypeProxy()
        if schema is True:
            type_: Type = NativeType("Any")
            if root:
                assert self.root is not None
                self.root.set_type(type_)
            return type_
        if schema is False:
            type_ = BuiltinType("None")
            if root:
                assert self.root is not None
                self.root.set_type(type_)
            return type_
        assert not isinstance(schema, bool)

        no_title = (
            "$ref" in schema or "$recursiveRef" in schema or "$dynamicRef" in schema or "allOf" in schema
        )

        proxy = TypeProxy()

        self.get_type_start(schema, proxy, proposed_name)

        the_type = self.build_type(schema, proposed_name)
        assert the_type is not None

        if not no_title:
            description = get_description(schema_meta_data)

            additional_description = the_type.comments()
            if description and additional_description:
                description.append("")
            description += additional_description
            if description:
                if auto_alias:
                    alias = True
                    if isinstance(the_type, NamedType):
                        alias = False
                    elif isinstance(the_type, CombinedType):
                        alias = not isinstance(the_type.base, NamedType)
                    if alias:
                        the_type = TypeAlias(
                            self.get_name(schema_meta_data, proposed_name),
                            the_type,
                            description,
                        )
                the_type.set_comments(description)

        if "default" in schema_meta_data:
            the_type.add_depends_on(
                Constant(
                    f"{self.get_name(schema_meta_data, proposed_name, upper=True)}_DEFAULT",
                    schema_meta_data["default"],
                    [f"Default value of the field path '{proposed_name}'"],
                ),
            )

        proxy.set_type(the_type)
        if root:
            assert self.root is not None
            self.root.set_type(the_type)

        self.get_type_end(schema, proxy)

        return the_type

    def get_name(
        self,
        schema: Optional[
            Union[
                jsonschema_draft_04.JSONSchemaD4,
                jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
            ]
        ],
        proposed_name: Optional[str] = None,
        upper: bool = False,
        postfix: Optional[str] = None,
    ) -> str:
        """Get the Python name for schema element."""
        return get_name(schema, proposed_name, upper, self.get_name_properties, postfix=postfix)

    def resolve_ref(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """Resolve a reference in the schema."""
        schema_core = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            schema,
        )
        if "$ref" in schema_core:
            return cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                self.resolver.lookup(schema_core["$ref"]),
            )
        return schema

    def build_type(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        proposed_name: str,
    ) -> Type:
        """Get a :class:`.Type` for a JSON schema."""
        schema_meta_data = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
            schema,
        )
        schema_core = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            schema,
        )

        proposed_name = schema_meta_data.get("title", proposed_name)

        if "if" in schema:
            schema.setdefault("used", set()).add("if")  # type: ignore[typeddict-item]
            base_schema = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                {},
            )
            base_schema.update(schema)  # type: ignore[typeddict-item]
            for key in ("if", "then", "else", "title", "description"):
                if key in base_schema:
                    del base_schema[key]  # type: ignore[misc]
            then_schema = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                {},
            )
            then_schema.update(base_schema)  # type: ignore[typeddict-item]
            schema.setdefault("used", set()).add("then")  # type: ignore[typeddict-item]
            then_schema.update(
                self.resolve_ref(  # type: ignore[typeddict-item]
                    cast(
                        "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                        schema.get("then", {}),
                    ),
                ),
            )
            if "properties" not in then_schema:
                then_schema["properties"] = {}
            then_properties = then_schema["properties"]
            then_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
            assert then_properties
            if_schema = self.resolve_ref(
                cast(
                    "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                    schema.get("if", {}),
                ),
            )
            if_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]
            if_properties = if_schema.get("properties", {})
            assert if_properties
            then_properties.update(if_properties)  # type: ignore[arg-type]
            else_schema = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                {},
            )
            else_schema.update(base_schema)  # type: ignore[typeddict-item]
            schema.setdefault("used", set()).add("else")  # type: ignore[typeddict-item]
            original_else_schema = self.resolve_ref(
                cast(
                    "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                    schema.get("else", {}),
                ),
            )
            else_schema.update(original_else_schema)  # type: ignore[typeddict-item]
            original_else_schema.setdefault("used", set()).add("properties")  # type: ignore[typeddict-item]

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
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
            schema,
        )
        schema_validation = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_validation.JSONSchemaItemD2020]",
            schema,
        )

        if "allOf" in schema and self.significative_sub_type(schema["allOf"]):
            type_, named_types, _ = self.all_of(
                schema,
                schema["allOf"],
                proposed_name,
                "allof",
            )
            if named_types:
                for named_type in named_types:
                    type_.add_depends_on(named_type)
                additional_type_str = [t.name(self.python_version) for t in named_types]
                type_.comments().append(f"Subtype: {', '.join(additional_type_str)}")

            return type_
        if "anyOf" in schema and self.significative_sub_type(schema["anyOf"]):
            schema.setdefault("used", set()).add("anyOf")  # type: ignore[typeddict-item]
            type_, named_types, _ = self.any_of(
                schema,
                schema["anyOf"],
                proposed_name,
                "anyof",
            )
            if not isinstance(type_, NamedType):
                type_ = TypeAlias(self.get_name(schema_meta_data, proposed_name), type_)
            elif type_.comments():
                type_.comments().append("")
            type_.comments().append("Aggregation type: anyOf")

            if named_types:
                for named_type in named_types:
                    type_.add_depends_on(named_type)
                additional_type_str = [t.name(self.python_version) for t in named_types]
                type_.comments().append(f"Subtype: {', '.join(additional_type_str)}")

            return type_
        if "oneOf" in schema and self.significative_sub_type(schema["oneOf"]):
            schema.setdefault("used", set()).add("oneOf")  # type: ignore[typeddict-item]
            type_, named_types, _ = self.any_of(
                schema,
                schema["oneOf"],
                proposed_name,
                "oneof",
            )
            if type_.comments():
                type_.comments().append("")
            type_.comments().append("Aggregation type: oneOf")

            if named_types:
                for named_type in named_types:
                    type_.add_depends_on(named_type)
                additional_type_str = [t.name(self.python_version) for t in named_types]
                type_.comments().append(f"Subtype: {', '.join(additional_type_str)}")
            return type_
        if "enum" in schema:
            return self.enum(schema_validation, proposed_name)

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
        schema_type = schema.get("type", ["string", "number", "object", "array", "boolean", "null"])
        if isinstance(schema_type, list) and len(schema_type) == 1:
            schema_type = schema_type[0]

        if isinstance(schema_type, list):
            if len(schema_type) == 0:
                return BuiltinType("None")
            name = self.get_name(schema_meta_data, proposed_name)
            has_title = "title" in schema_meta_data
            proposed_name = schema_meta_data.get("title", proposed_name)

            schema_copy = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                dict(schema),
            )
            schema_meta_data_copy = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
                schema_copy,
            )
            if "title" in schema_meta_data_copy:
                del schema_meta_data_copy["title"]

            inner_types = [
                self._get_type(schema_copy, cast("str", primitive_type), f"{proposed_name} {primitive_type}")
                for primitive_type in schema_type
            ]
            type_ = UnionType(inner_types)
            if has_title:
                type_ = TypeAlias(name, type_)
            return type_

        if isinstance(schema_type, str):
            return self._get_type(schema, schema_type, proposed_name)

        if "default" in schema:
            return self.default(schema_meta_data, proposed_name)

        type_ = BuiltinType("Any")
        type_.set_comments(["WARNING: we get an schema without any type"])
        return type_

    def _get_type(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        schema_type: str,
        proposed_name: str,
    ) -> Type:
        schema_meta_data = cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019]",
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
            ],
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
        """
        Treat the anyOf keyword.

        See: https://json-schema.org/understanding-json-schema/reference/combining.html#anyof.
        """

    def significative_sub_type(
        self,
        sub_schemas: Union[
            list[jsonschema_draft_04.JSONSchemaD4],
            list[jsonschema_draft_2020_12_applicator.JSONSchemaD2020],
        ],
    ) -> bool:
        """Are the the subtype significative."""
        if not sub_schemas:
            return False
        for sub_schema in sub_schemas:
            assert not isinstance(sub_schema, bool)
            sub_schema = self.resolve_ref(sub_schema)  # noqa: PLW2901
            for prop in ["type", "properties", "items", "additionalProperties", "enum"]:
                if prop in sub_schema:
                    return True
        return False

    @abstractmethod
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
        """
        Thread the allOf keyword.

        See: https://json-schema.org/understanding-json-schema/reference/combining.html#allof.
        """

    @abstractmethod
    def enum(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_validation.JSONSchemaItemD2020,
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
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
        ],
        proposed_name: str,
    ) -> Type:
        """
        Treat the default  keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """
