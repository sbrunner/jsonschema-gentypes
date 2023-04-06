"""
Generate the type structure based on the Type class from the JSON schema file.
"""

import keyword
import re
import textwrap
import unicodedata
from abc import abstractmethod
from io import StringIO
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

import ruamel.yaml
from jsonschema import RefResolver

from jsonschema_gentypes import configuration, jsonschema

# Raise issues here.
ISSUE_URL = "https://github.com/camptcamp/jsonschema-gentypes"


def __pinyin(char: str) -> str:
    try:
        import pinyin  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        return char

    char = pinyin.get(char, delimiter=" ")
    return (
        char
        if len(char) == 1
        else "".join([c for c in unicodedata.normalize("NFKD", f" {char} ") if not unicodedata.combining(c)])
    )


def __romkan(char: str) -> str:
    try:
        import romkan  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        return char

    return cast(str, romkan.to_roma(char))


def __greek(char: str) -> str:
    try:
        import romanize  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        return char

    return cast(str, romanize.romanize(char))


def __char_range(char1: str, char2: str) -> List[str]:
    """
    Generate the characters range from `char1` to `char2`, inclusive.

    Arguments:
        char1: the first char of the range
        char2: the last char of the range
    """
    return [chr(char) for char in range(ord(char1), ord(char2) + 1)]


AUTHORIZED_CHAR = __char_range("a", "z") + __char_range("A", "Z") + __char_range("0", "9")


def __convert_char(char: str) -> str:
    if char in AUTHORIZED_CHAR:
        return char

    # Remove accents
    if unicodedata.combining(char):
        return ""
    if char == "-":
        return " "
    category = unicodedata.category(char)
    # All spaced => space
    if category in ("Zs", "Cc"):
        return " "
    # Explicit sign
    if category in ("So", "Po"):
        name = unicodedata.name(char)
        if category == "So":
            name = name.replace(" SIGN", "")
        return f" {name} "

    # Greek characters
    char = __greek(char)
    if char in AUTHORIZED_CHAR or len(char) > 1:
        return char

    # Japanese characters
    char = __romkan(char)
    if char in AUTHORIZED_CHAR or len(char) > 1:
        return char

    # Chinese characters
    char = __pinyin(char)
    if char in AUTHORIZED_CHAR or len(char) > 1:
        return char

    return " "


def normalize(input_str: str) -> str:
    """Normalize the string to be a Python name."""

    # Unaccent, ...
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    name = "".join([__convert_char(c) for c in nfkd_form])

    # No number at first position
    if name[0] in __char_range("0", "9"):
        name = f"num {name}"

    # No python keyword
    if name in keyword.kwlist:
        name = f"{name} name"
    return name


class Type:
    """
    The base Type object.
    """

    _comments: Optional[List[str]] = None
    _depends_on: Optional[List["Type"]] = None

    def __init__(self) -> None:
        """
        Initialize the type.
        """
        self._depends_on = []

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        raise NotImplementedError

    def imports(self, python_version: Tuple[int, ...]) -> List[Tuple[str, str]]:
        """
        Return the needed imports.
        """
        del python_version
        return []

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Return the type declaration.

        Arguments:
            line_length: the maximum line length
        """
        del line_length
        return []

    def depends_on(self) -> List["Type"]:
        """
        Return the needed sub types.
        """
        assert self._depends_on is not None
        return self._depends_on

    def add_depends_on(self, depends_on: "Type") -> None:
        """
        Add a sub type.
        """
        assert self._depends_on is not None
        self._depends_on.append(depends_on)

    def comments(self) -> List[str]:
        """
        Additional comments shared by the type.
        """
        if self._comments is None:
            self._comments = []
        return self._comments

    def set_comments(self, comments: List[str]) -> None:
        """
        Set comment on the type.
        """
        self._comments = comments


class NamedType(Type):
    """
    The based type of named type.
    """

    def __init__(self, name: str) -> None:
        """
        Init.

        Arguments:
            name: the type name
        """
        super().__init__()
        self._name = name

    def postfix_name(self, postfix: str) -> None:
        """
        Set a new name (Not available every time).
        """
        self._name += postfix

    def set_name(self, name: str) -> None:
        """
        Set a new name (Not available every time).
        """
        self._name = name

    def unescape_name(self) -> str:
        """
        Return the unescaped name.
        """
        return self._name

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        return f'"{self._name}"'


class LiteralType(Type):
    """
    A literal type like: `Literal["text"]`.
    """

    def __init__(self, const: Union[int, float, bool, str, None]) -> None:
        """
        Init.

        Arguments:
            const: the constant
        """
        super().__init__()
        self.const = const

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        if isinstance(self.const, str):
            return f'Literal["{self.const}"]'
        else:
            return f"Literal[{self.const}]"

    def imports(self, python_version: Tuple[int, ...]) -> List[Tuple[str, str]]:
        """
        Return the needed imports.
        """
        del python_version
        return [("typing", "Literal")]


class BuiltinType(Type):
    """
    Python builtin type, e.g.: str.
    """

    def __init__(self, name: str) -> None:
        """
        Init.

        Arguments:
            name: the type name
        """
        super().__init__()
        self._name = name

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        return self._name


class NativeType(Type):
    """
    Native Type that will essentially generates a Python import.
    """

    def __init__(
        self,
        name: str,
        package: str = "typing",
        minimal_python_version: Optional[Tuple[int, ...]] = None,
        workaround_package: Optional[str] = None,
    ) -> None:
        """
        Init.

        Arguments:
            name: the type name
            package: the package of the type
            minimal_python_version: the minimal Python version to use the type
            workaround_package: the package to use if the minimal Python version is not met
        """
        super().__init__()
        self.package = package
        self._name = name
        self.minimal_python_version = minimal_python_version
        self.workaround_package = workaround_package

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        return self._name

    def imports(self, python_version: Tuple[int, ...]) -> List[Tuple[str, str]]:
        """
        Return the needed imports.
        """
        if self.minimal_python_version is not None and python_version < self.minimal_python_version:
            assert self.workaround_package is not None
            return [(self.workaround_package, self._name)]
        return [(self.package, self._name)]


class CombinedType(Type):
    """
    A combined type.

    e.g.: Union[str, int] is an Combined type of `str` and `int` with `Union` as base.
    """

    def __init__(self, base: Type, sub_types: List[Type]) -> None:
        """
        Init.

        Arguments:
            base: the base type (e.-g. for `Union[str, int]` the base type is `Union`)
            sub_types: the sub types (e.-g. for `Union[str]` the sub types are `str` and `int`)
        """
        super().__init__()
        self.base = base
        self.sub_types = sub_types
        self.name()

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        assert isinstance(self.base, Type)
        return f"{self.base.name()}[{', '.join([sub_type.name() for sub_type in self.sub_types])}]"

    def depends_on(self) -> List[Type]:
        """
        Return the needed sub types.
        """
        return [self.base] + self.sub_types + super().depends_on()


class TypeAlias(NamedType):
    """
    An alias on a type, essentially to add a description.
    """

    def __init__(self, name: str, sub_type: Type, descriptions: Optional[List[str]] = None):
        """
        Init.

        Arguments:
            name: the type name
            sub_type: the type that should be aliased
            descriptions: the type description
        """
        super().__init__(name)
        self.sub_type = sub_type
        self.descriptions = [] if descriptions is None else descriptions

    def depends_on(self) -> List[Type]:
        """
        Return the needed sub types.
        """
        return [self.sub_type] + super().depends_on()

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Return the type declaration.
        """
        result = ["", ""]
        result.append(f"{self._name} = {self.sub_type.name()}")
        comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
        if len(comments) == 1:
            result += [f'"""{comments[0]}"""', ""]
        elif comments:
            result += ['"""', *comments, '"""', ""]

        return result


class TypeEnum(NamedType):
    """
    The Type that represent an Enum in Python.
    """

    def __init__(self, name: str, values: List[Union[int, float, bool, str, None]], descriptions: List[str]):
        """
        Init.

        Arguments:
            name: the type name
            values: the values of the enum
            descriptions: the type description
        """
        assert len(values) > 0
        super().__init__(name)
        self.values = values
        self.descriptions = descriptions
        self.sub_type: Type = CombinedType(NativeType("Union"), [LiteralType(value) for value in values])

    def depends_on(self) -> List["Type"]:
        """
        Return the needed sub types.
        """
        return [self.sub_type] + super().depends_on()

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Return the type declaration.
        """
        result = ["", ""]
        comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
        result.append(f"{self._name} = {self.sub_type.name()}")
        if len(comments) == 1:
            result += [f'"""{comments[0]}"""']
        elif comments:
            result += ['"""', *comments, '"""']
        for value in self.values:
            name = get_name({"title": f"{self._name} {value}"}, upper=True)
            formatted_value = f'"{value}"' if isinstance(value, str) else str(value)
            result.append(f"{name}: {LiteralType(value).name()} = {formatted_value}")
            name = self.descriptions[0] if self.descriptions else self._name
            if name.endswith("."):
                name = name[:-1]
            result.append(f'"""The values for the \'{name}\' enum"""')

        result.append("")
        return result


class TypedDictType(NamedType):
    """
    The Type that represent a TypedDict in Python.
    """

    def __init__(
        self,
        name: str,
        struct: Dict[str, Type],
        descriptions: List[str],
        required: Set[str],
    ):
        """
        Init.

        Arguments:
            name: name of the type
            struct: the struct of the subtypes
            descriptions: the description
            required: the required properties names
        """
        super().__init__(name)
        self.descriptions = descriptions

        def get_required_type(prop_type: Type) -> Type:
            result = CombinedType(NativeType("Required", "typing", (3, 11), "typing_extensions"), [prop_type])
            if prop_type.comments():
                result.set_comments([*prop_type.comments(), "", "Required property"])
            else:
                result.set_comments(["Required property"])
            return result

        self.struct = {
            name: get_required_type(prop_type) if name in required else prop_type
            for name, prop_type in struct.items()
        }

    def depends_on(self) -> List[Type]:
        """
        Get the types that we requires to be valid.
        """
        result: List[Type] = [NativeType("TypedDict")]
        result += self.struct.values()
        return result + super().depends_on()

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Get the definition based on a dict.
        """
        supported_re = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        # Support to be a class
        supported = True

        for property_ in self.struct.keys():
            if not supported_re.match(property_) or property_ in keyword.kwlist:
                supported = False
                break

        result = ["", ""]
        if supported:
            result.append(f"class {self._name}(TypedDict, total=False):")
            comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
            if len(comments) == 1:
                result.append(f'    """{comments[0]}"""')
                result.append("")
            elif comments:
                result.append('    """')
                result += [f"    {d}" if d else "" for d in comments]
                result.append('    """')
                result.append("")

            for property_, type_obj in self.struct.items():
                result.append(f"    {property_}: {type_obj.name()}")
                comments = type_obj.comments()
                if len(comments) == 1:
                    result.append(f'    """{comments[0]}"""')
                    result.append("")
                elif comments:
                    result.append('    """')
                    result += [f"    {comment}" if comment else "" for comment in comments]
                    result.append('    """')
                    result.append("")
        else:
            result += [
                "# " + d for d in split_comment(self.descriptions, line_length - 2 if line_length else None)
            ]
            result.append(f"{self._name} = TypedDict('{self._name}', " + "{")
            for property_, type_obj in self.struct.items():
                result += [f"    # {comment}" for comment in type_obj.comments()]
                result.append(f"    '{property_}': {type_obj.name()},")
            result.append("}, total=False)")
        return result


class Constant(NamedType):
    """
    The Pseudo Type is used to add the default constants.
    """

    def __init__(self, name: str, constant: Any, descriptions: List[str]):
        """
        Init.

        Arguments:
            name: the type name
            constant: the constant value
            descriptions: the type description
        """
        super().__init__(name)
        self.constant = constant
        self.descriptions = descriptions

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Return the type declaration.
        """
        result = ["", ""]
        if isinstance(self.constant, dict) and not self.constant:
            result.append(f"{self._name}: Dict[str, Any] = {repr(self.constant)}")
        elif isinstance(self.constant, (dict, list)) and not self.constant:
            result.append(f"{self._name}: List[Any] = {repr(self.constant)}")
        else:
            result.append(f"{self._name} = {repr(self.constant)}")
        comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
        if len(comments) == 1:
            result += [f'"""{comments[0]}"""', ""]
        elif comments:
            result += ['"""', *comments, '"""', ""]
        return result

    def imports(self, python_version: Tuple[int, ...]) -> List[Tuple[str, str]]:
        """
        Return the needed imports.
        """
        del python_version

        if isinstance(self.constant, dict) and not self.constant:
            return [("typing", "Any"), ("typing", "Dict")]
        elif isinstance(self.constant, list) and not self.constant:
            return [("typing", "Any"), ("typing", "List")]
        else:
            return []


def split_comment(text: List[str], line_length: Optional[int]) -> List[str]:
    """
    Split the text at line length.

    Arguments:
        text: the lines to split
        line_length: the maximum line length
    """
    if not line_length:
        return text

    result = []
    for line in text:
        # Don't remove empty lines
        if line:
            result += textwrap.wrap(line, width=line_length, break_long_words=False)
        else:
            result.append(line)
    return result


def get_name(
    schema: Optional[jsonschema.JSONSchemaItem],
    proposed_name: Optional[str] = None,
    upper: bool = False,
) -> str:
    """
    Get the name for an element.

    Arguments:
        schema: the concerned schema
        proposed_name: a name that we will use it the schema hasn't any title
        upper: should we use an upper case (For constants)
    """
    # Get the base name
    has_title = isinstance(schema, dict) and "title" in schema
    name = schema["title"] if has_title else proposed_name  # type: ignore
    assert name is not None
    name = normalize(name)

    prefix = "" if has_title else "_"
    if upper:
        # Upper case
        name = name.upper()
        # Remove spaces
        return prefix + "".join(["_" if char.isspace() else char for char in name])
    else:
        # Title case
        name = name.title()
        # Remove spaces
        return prefix + "".join([char for char in name if not char.isspace()])


def get_description(schema: jsonschema.JSONSchemaItem) -> List[str]:
    """
    Get the standard description for an element.

    Arguments:
        schema: the concerned schema
    """
    yaml = ruamel.yaml.YAML(typ="safe")
    yaml.default_flow_style = False

    result: List[str] = []
    if "title" in schema:
        result.append(f"{schema['title']}.")
    if "description" in schema:
        if result:
            result.append("")
        result += schema["description"].split("\n")
    first = True
    for key, value in schema.items():
        if (
            key
            not in (
                "title",
                "description",
                "$ref",
                "$schema",
                "$id",
                "const",
                "type",
                "items",
                "additionalProperties",
            )
            and not isinstance(value, list)
            and not isinstance(value, dict)
        ):
            if first:
                if result:
                    result.append("")
                first = False
            result.append(f"{key}: {value}")
        elif key in (
            "not",
            "default",
            "examples",
            "contains",
            "patternProperties",
            "dependencies",
            "propertyNames",
        ):
            if first:
                if result:
                    result.append("")
                first = False
            result.append(f"{key}:")
            formatted_value = StringIO()
            yaml.dump(value, formatted_value)
            result += [f"  {line}" for line in formatted_value.getvalue().split("\n") if line]

    return result


class API:
    """
    Base class for JSON schema types API.
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
        self.base_name = "Base"
        self.recursive_anchor_path: List[str] = []

    def set_base_name(self, name: str) -> None:
        """
        Set the name of the base element.
        """
        self.base_name = name

    def get_type_handler(self, schema_type: str) -> Callable[[jsonschema.JSONSchemaItem, str], Type]:
        """
        Get a handler from this schema draft version.
        """
        if schema_type.startswith("_"):
            raise AttributeError("No way friend")
        handler = cast(Callable[[jsonschema.JSONSchemaItem, str], Type], getattr(self, schema_type, None))
        if handler is None:
            raise NotImplementedError(
                f"Type `{schema_type}` is not supported. If you think that this is an error, "
                f"say something at {ISSUE_URL}"
            )
        return handler

    def get_type(
        self, schema: jsonschema.JSONSchema, proposed_name: Optional[str] = None, auto_alias: bool = True
    ) -> Type:
        """
        Get a :class:`.Type` for a JSON schema.
        """
        if schema is True:
            return NativeType("Any")
        if schema is False:
            return BuiltinType("None")
        assert not isinstance(schema, bool)

        if proposed_name is None:
            proposed_name = self.base_name

        if schema.get("$recursiveAnchor", False):
            self.recursive_anchor_path.append(get_name(schema, proposed_name))

        the_type = self._get_type_internal(schema, proposed_name)
        assert the_type is not None
        additional_description = the_type.comments()
        description = get_description(schema)
        if description and additional_description:
            description.append("")
        description += additional_description
        if not isinstance(the_type, NamedType) and description:
            if auto_alias:
                the_type = TypeAlias(get_name(schema, proposed_name), the_type, description)
            else:
                the_type.set_comments(description)

        if "default" in schema:
            the_type.add_depends_on(
                Constant(
                    f"{get_name(schema, proposed_name, True)}_DEFAULT",
                    schema["default"],
                    [f"Default value of the field path '{proposed_name}'"],
                )
            )

        if schema.get("$recursiveAnchor", False):
            self.recursive_anchor_path.pop()

        return the_type

    def _resolve_ref(self, schema: jsonschema.JSONSchemaItem) -> jsonschema.JSONSchemaItem:
        if "$ref" in schema:
            with self.resolver.resolving(schema["$ref"]) as resolved:
                schema.update(resolved)
        return schema

    def _get_type_internal(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Get a :class:`.Type` for a JSON schema.
        """

        scope = schema.get("$id", "")
        if scope:
            self.resolver.push_scope(scope)
        proposed_name = schema.get("title", proposed_name)

        if "if" in schema:
            base_schema: jsonschema.JSONSchemaItem = {}
            base_schema.update(schema)
            for key in ("if", "then", "else", "title", "description"):
                if key in base_schema:
                    del base_schema[key]  # type: ignore
            then_schema: jsonschema.JSONSchemaItem = {}
            then_schema.update(base_schema)
            then_schema.update(self._resolve_ref(cast(jsonschema.JSONSchemaItem, schema.get("then", {}))))
            if "properties" not in then_schema:
                then_schema["properties"] = {}
            then_properties = then_schema["properties"]
            assert then_properties
            if_properties = self._resolve_ref(cast(jsonschema.JSONSchemaItem, schema.get("if", {}))).get(
                "properties", {}
            )
            assert if_properties
            then_properties.update(if_properties)
            else_schema: jsonschema.JSONSchemaItem = {}
            else_schema.update(base_schema)
            else_schema.update(self._resolve_ref(cast(jsonschema.JSONSchemaItem, schema.get("else", {}))))

            return CombinedType(
                NativeType("Union"),
                [
                    self.get_type(then_schema, proposed_name + " then"),
                    self.get_type(else_schema, proposed_name + " else"),
                ],
            )

        if "$ref" in schema or "$recursiveRef" in schema:
            return self.ref(schema, proposed_name)

        if "const" in schema:
            return self.const(schema, proposed_name)

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
            proposed_name = schema.get("title", proposed_name)
            schema_copy = cast(jsonschema.JSONSchemaItem, dict(schema))
            if "title" in schema_copy:
                del schema_copy["title"]
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
                    schema, cast(List[jsonschema.JSONSchemaItem], schema["allOf"]), proposed_name, "allof"
                )
                if type_.comments():
                    type_.comments().append("")
                type_.comments().append("WARNING: PEP 544 does not support an Intersection type,")
                type_.comments().append("so `allOf` is interpreted as a `Union` for now.")
                type_.comments().append("See: https://github.com/camptocamp/jsonschema-gentypes/issues/8")
                return type_
            elif "anyOf" in schema:
                return self.any_of(
                    schema, cast(List[jsonschema.JSONSchemaItem], schema["anyOf"]), proposed_name, "anyof"
                )
            elif "oneOf" in schema:
                type_ = self.any_of(
                    schema, cast(List[jsonschema.JSONSchemaItem], schema["oneOf"]), proposed_name, "oneof"
                )
                if type_.comments():
                    type_.comments().append("")
                type_.comments().append("oneOf")
                return type_
            elif "enum" in schema:
                return self.enum(schema, proposed_name)
            elif "default" in schema:
                return self.default(schema, proposed_name)
        if scope:
            self.resolver.pop_scope()

        if schema_type is None:
            type_ = BuiltinType("None")
            type_.set_comments(["WARNING: we get an schema without any type"])
            return type_
        assert isinstance(schema_type, str), (
            f"Expected to find a supported schema type, got {schema_type}" f"\nDuring parsing of {schema}"
        )

        return self._get_type(schema, schema_type, proposed_name)

    def _get_type(self, schema: jsonschema.JSONSchemaItem, schema_type: str, proposed_name: str) -> Type:
        proposed_name = schema.get("title", proposed_name)

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
    def ref(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Treat the ref keyword.

        See: https://json-schema.org/understanding-json-schema/structuring.html.
        """

    @abstractmethod
    def any_of(
        self,
        schema: jsonschema.JSONSchemaItem,
        sub_schema: List[jsonschema.JSONSchemaItem],
        proposed_name: str,
        sub_name: str,
    ) -> Type:
        """
        Treat the anyOf keyword.

        See: https://json-schema.org/understanding-json-schema/reference/combining.html#anyof.
        """

    @abstractmethod
    def const(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Treat the const  keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html#constant-values
        """

    @abstractmethod
    def enum(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Treat enum.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html#enumerated-values
        """

    @abstractmethod
    def default(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Treat the default  keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """


class APIv4(API):
    """
    JSON Schema draft 4.
    """

    def const(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate a ``Literal`` for a const value.
        """
        const_: Union[int, float, str, bool, None] = schema["const"]
        return LiteralType(const_)

    def enum(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate an enum.
        """
        return TypeEnum(
            get_name(schema, proposed_name),
            cast(List[Union[int, float, bool, str, None]], schema["enum"]),
            get_description(schema),
        )

    def boolean(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate a ``bool`` annotation for a boolean object.
        """
        del schema, proposed_name
        return BuiltinType("bool")

    def object(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate an annotation for an object, usually a TypedDict.
        """

        std_dict = None
        name = get_name(schema, proposed_name)
        additional_properties = cast(jsonschema.JSONSchema, schema.get("additionalProperties"))
        if (
            additional_properties is True
            and self.additional_properties == configuration.ADDITIONALPROPERTIES_ALWAYS
        ):
            std_dict = CombinedType(NativeType("Dict"), [BuiltinType("str"), NativeType("Any")])
        elif isinstance(additional_properties, dict):
            sub_type = self.get_type(additional_properties, f"{proposed_name} additionalProperties")
            std_dict = CombinedType(NativeType("Dict"), [BuiltinType("str"), sub_type])
        properties = cast(Dict[str, jsonschema.JSONSchemaItem], schema.get("properties"))
        proposed_name = schema.get("title", proposed_name)
        if properties:
            required = set(schema.get("required", []))

            struct = {
                prop: self.get_type(sub_schema, proposed_name + " " + prop, auto_alias=False)
                for prop, sub_schema in properties.items()
            }

            type_: Type = TypedDictType(
                name if std_dict is None else name + "Typed",
                struct,
                get_description(schema) if std_dict is None else [],
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

    def array(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate a ``List[]`` annotation with the allowed types.
        """
        items = schema.get("items")
        if items is True:
            return CombinedType(NativeType("List"), [NativeType("Any")])
        elif items is False:
            raise NotImplementedError('"items": false is not supported')
        elif isinstance(items, list):
            inner_types = [self.get_type(cast(jsonschema.JSONSchemaItem, item)) for item in items]
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
            return type_
        elif items is not None:
            return CombinedType(
                NativeType("List"),
                [self.get_type(cast(jsonschema.JSONSchemaItem, items), proposed_name + " item")],
            )
        else:
            type_ = BuiltinType("None")
            type_.set_comments(["WARNING: we get an array without any items"])
            return type_

    def any_of(
        self,
        schema: jsonschema.JSONSchemaItem,
        sub_schema: List[jsonschema.JSONSchemaItem],
        proposed_name: str,
        sub_name: str,
    ) -> Type:
        """
        Generate a ``Union`` annotation with the allowed types.
        """
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

    def ref(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Handle a `$ref`.
        """

        if schema.get("$recursiveRef") == "#":
            return NamedType(self.recursive_anchor_path[-1])

        ref = schema["$ref"]
        del schema["$ref"]

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

            return NamedType(self.base_name)

        if ref in self.ref_type:
            return self.ref_type[ref]

        resolve = getattr(self.resolver, "resolve", None)
        if resolve is None:
            with self.resolver.resolving(ref) as resolved:
                schema.update(resolved)
                type_ = self.get_type(schema)
        else:
            scope, resolved = self.resolver.resolve(ref)
            self.resolver.push_scope(scope)
            try:
                schema.update(resolved)
                type_ = self.get_type(schema, proposed_name)
            finally:
                self.resolver.pop_scope()

        if ref:
            self.ref_type[ref] = type_
        return type_

    def string(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate a ``str`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("str")

    def number(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate a ``Union[int, float]`` annotation.
        """
        del schema, proposed_name
        return CombinedType(NativeType("Union"), [BuiltinType("int"), BuiltinType("float")])

    def integer(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate an ``int`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("int")

    def null(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Generate an ``None`` annotation.
        """
        del schema, proposed_name
        return BuiltinType("None")

    def default(self, schema: jsonschema.JSONSchemaItem, proposed_name: str) -> Type:
        """
        Treat the default keyword.

        See: https://json-schema.org/understanding-json-schema/reference/generic.html
        """

        type_ = "Any"
        for test_type, type_name in [
            (str, "str"),
            (int, "int"),
            (float, "float"),
            (bool, "bool"),
        ]:
            if isinstance(schema["default"], test_type):
                type_ = type_name
        the_type = BuiltinType(type_)
        return the_type


class APIv6(APIv4):
    """
    JSON Schema draft 6.
    """


class APIv7(APIv6):
    """
    JSON Schema draft 7.
    """
