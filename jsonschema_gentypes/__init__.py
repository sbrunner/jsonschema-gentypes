"""Generate the type structure based on the Type class from the JSON schema file."""

import keyword
import random
import re
import textwrap
import unicodedata
from typing import Any, Optional, Union, cast

import yaml

from jsonschema_gentypes import jsonschema_draft_04, jsonschema_draft_2019_09_meta_data


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


def __unidecode(char: str) -> str:
    try:
        import unidecode  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        return char

    return unidecode.unidecode(char)


def __greek(char: str) -> str:
    try:
        import romanize  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        return char

    return cast("str", romanize.romanize(char))


def __char_range(char1: str, char2: str) -> list[str]:
    """
    Generate the characters range from `char1` to `char2`, inclusive.

    Parameter:
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

    # Chinese characters
    char = __pinyin(char)
    if char in AUTHORIZED_CHAR or len(char) > 1:
        return char

    # Other characters
    char = __unidecode(char)
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
    """The base Type object."""

    _comments: Optional[list[str]] = None
    _depends_on: Optional[list["Type"]] = None

    def __init__(self) -> None:
        """Initialize the type."""
        self._depends_on = []

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        raise NotImplementedError

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        del python_version
        return []

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """
        Return the type declaration.

        Parameter:
            line_length: the maximum line length
        """
        del line_length, python_version
        return []

    def depends_on(self, python_version: tuple[int, ...]) -> list["Type"]:
        """Return the needed sub types."""
        del python_version
        assert self._depends_on is not None
        return self._depends_on

    def add_depends_on(self, depends_on: "Type") -> None:
        """Add a sub type."""
        assert self._depends_on is not None
        self._depends_on.append(depends_on)

    def comments(self) -> list[str]:
        """Additional comments shared by the type."""
        if self._comments is None:
            self._comments = []
        return self._comments

    def set_comments(self, comments: list[str]) -> None:
        """Set comment on the type."""
        self._comments = comments


class TypeProxy(Type):
    """A proxy on a type that can be set later."""

    _type: Optional[Type] = None

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        assert self._type is not None
        return self._type.name(python_version)

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        assert self._type is not None
        return self._type.imports(python_version)

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """
        Return the type declaration.

        Parameter:
            line_length: the maximum line length
        """
        del line_length
        assert self._type is not None
        return self._type.definition(python_version)

    def depends_on(self, python_version: tuple[int, ...]) -> list["Type"]:
        """Return the needed sub types."""
        assert self._type is not None
        return self._type.depends_on(python_version)

    def comments(self) -> list[str]:
        """Additional comments shared by the type."""
        return self._type.comments() if self._type is not None else []

    def set_comments(self, comments: list[str]) -> None:
        """Set comment on the type."""
        print(f"Warning: set_comments on a TypeProxy, lost comments: {comments}")

    def set_type(self, type_: Type) -> None:
        """Set the type."""
        self._type = type_


class NamedType(Type):
    """The based type of named type."""

    def __init__(self, name: str) -> None:
        """
        Init.

        Parameter:
            name: the type name
        """
        super().__init__()
        self._name = name

    def postfix_name(self, postfix: str) -> None:
        """Set a new name (Not available every time)."""
        self._name += postfix

    def set_name(self, name: str) -> None:
        """Set a new name (Not available every time)."""
        self._name = name

    def unescape_name(self) -> str:
        """Return the unescaped name."""
        return self._name

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        del python_version
        return f'"{self._name}"'


class LiteralType(Type):
    """A literal type like: `Literal["text"]`."""

    def __init__(self, const: Union[float, bool, str, None, dict[str, Any], list[Any]]) -> None:
        """
        Init.

        Parameter:
            const: the constant
        """
        super().__init__()
        self.const = const

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        del python_version
        return f"Literal[{self.const!r}]"

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        del python_version
        return [("typing", "Literal")]


class BuiltinType(Type):
    """Python builtin type, e.g.: str."""

    def __init__(self, name: str) -> None:
        """
        Init.

        Parameter:
            name: the type name
        """
        super().__init__()
        self._name = name

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        del python_version
        return self._name


class NativeType(Type):
    """Native Type that will essentially generates a Python import."""

    def __init__(
        self,
        name: str,
        package: str = "typing",
        minimal_python_version: Optional[tuple[int, ...]] = None,
        workaround_package: Optional[str] = None,
    ) -> None:
        """
        Init.

        Parameter:
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

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        del python_version
        return self._name

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        if self.minimal_python_version is not None and python_version < self.minimal_python_version:
            assert self.workaround_package is not None
            return [(self.workaround_package, self._name)]
        return [(self.package, self._name)]

    def __repr__(self) -> str:
        """Get the representation of the object."""
        return f"NativeType({self.package!r}.{self._name!r})"


class CombinedType(Type):
    """
    A combined type.

    e.g.: Union[str, int] is an Combined type of `str` and `int` with `Union` as base.
    """

    def __init__(self, base: Type, sub_types: list[Type]) -> None:
        """
        Init.

        Parameter:
            base: the base type (e.-g. for `Union[str, int]` the base type is `Union`)
            sub_types: the sub types (e.-g. for `Union[str]` the sub types are `str` and `int`)
        """
        super().__init__()
        self.base = base
        self.sub_types = sub_types

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        assert isinstance(self.base, Type)
        return f"{self.base.name(python_version)}[{', '.join([sub_type.name(python_version) for sub_type in self.sub_types])}]"

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        return [self.base, *self.sub_types, *super().depends_on(python_version)]


class UnionType(CombinedType):
    """A Union type."""

    def __init__(self, sub_types: list[Type]) -> None:
        """
        Init.

        Parameter:
            sub_types: the sub types
        """
        super().__init__(NativeType("Union"), sub_types)

    def _required_union(self, python_version: tuple[int, ...]) -> bool:
        if python_version < (3, 10):
            return True
        return any(sub_type.name(python_version).startswith('"') for sub_type in self.sub_types)

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        if self._required_union(python_version):
            return super().depends_on(python_version)
        return [*self.sub_types, *super(CombinedType, self).depends_on(python_version)]

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        if self._required_union(python_version):
            return super().name(python_version)
        return f"{' | '.join([sub_type.name(python_version) for sub_type in self.sub_types])}"


class OptionalType(CombinedType):
    """An Optional type."""

    def __init__(self, sub_type: Type) -> None:
        """
        Init.

        Parameter:
            sub_type: the sub type
        """
        super().__init__(NativeType("Optional"), [sub_type])
        self.sub_type = sub_type

    def _required_optional(self, python_version: tuple[int, ...]) -> bool:
        if python_version < (3, 10):
            return True
        return self.sub_type.name(python_version).startswith('"')

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        if self._required_optional(python_version):
            return super().depends_on(python_version)
        return [self.sub_type, *super(CombinedType, self).depends_on(python_version)]

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        if self._required_optional(python_version):
            return super().name(python_version)
        return f"{self.sub_type.name(python_version)} | None"


class DictType(CombinedType):
    """A Dict type."""

    def __init__(self, key_type: Type, value_type: Type) -> None:
        """
        Init.

        Parameter:
            key_type: the key type
            value_type: the value type
        """
        super().__init__(NativeType("Dict"), [key_type, value_type])
        self.key_type = key_type
        self.value_type = value_type

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        if python_version < (3, 9):
            return super().depends_on(python_version)
        return [self.key_type, self.value_type, *super(CombinedType, self).depends_on(python_version)]

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        if python_version < (3, 9):
            return super().name(python_version)
        return f"dict[{self.key_type.name(python_version)}, {self.value_type.name(python_version)}]"


class ListType(CombinedType):
    """A List type."""

    def __init__(self, sub_type: Type) -> None:
        """
        Init.

        Parameter:
            sub_type: the sub type
        """
        super().__init__(NativeType("List"), [sub_type])
        self.sub_type = sub_type

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        if python_version < (3, 9):
            return super().depends_on(python_version)
        return [self.sub_type, *super(CombinedType, self).depends_on(python_version)]

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        if python_version < (3, 9):
            return super().name(python_version)
        return f"list[{self.sub_type.name(python_version)}]"


class TupleType(CombinedType):
    """A Tuple type."""

    def __init__(self, sub_types: list[Type]) -> None:
        """
        Init.

        Parameter:
            sub_types: the sub types
        """
        super().__init__(NativeType("Tuple"), sub_types)

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        if python_version < (3, 9):
            return super().depends_on(python_version)
        return [*self.sub_types, *super(CombinedType, self).depends_on(python_version)]

    def name(self, python_version: tuple[int, ...]) -> str:
        """Return what we need to use the type."""
        if python_version < (3, 9):
            return super().name(python_version)
        return f"tuple[{', '.join([sub_type.name(python_version) for sub_type in self.sub_types])}]"


class TypeAlias(NamedType):
    """An alias on a type, essentially to add a description."""

    def __init__(self, name: str, sub_type: Type, descriptions: Optional[list[str]] = None) -> None:
        """
        Init.

        Parameter:
            name: the type name
            sub_type: the type that should be aliased
            descriptions: the type description
        """
        super().__init__(name)
        self.sub_type = sub_type
        self._comments = [] if descriptions is None else descriptions

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Return the needed sub types."""
        return [self.sub_type, *super().depends_on(python_version)]

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """Return the type declaration."""
        result = ["", ""]
        _type = (
            ": TypeAlias"
            if isinstance(self.sub_type, BuiltinType) and self.sub_type.name(python_version) == "None"
            else ""
        )
        result.append(f"{self._name}{_type} = {self.sub_type.name(python_version)}")
        comments = split_comment(self.comments(), line_length - 2 if line_length else None)
        if len(comments) == 1:
            result += [f'""" {comments[0]} """', ""]
        elif comments:
            result += ['"""', *comments, '"""', ""]

        return result

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        return (
            [("typing", "TypeAlias")]
            if isinstance(self.sub_type, BuiltinType) and self.sub_type.name(python_version) == "None"
            else []
        )


class TypeEnum(NamedType):
    """The Type that represent an Enum in Python."""

    def __init__(
        self,
        name: str,
        values: list[Union[int, float, bool, str, None]],
        descriptions: list[str],
    ) -> None:
        """
        Init.

        Parameter:
            name: the type name
            values: the values of the enum
            descriptions: the type description
        """
        assert len(values) > 0
        super().__init__(name)
        self.values = values
        self.value_names = {value: get_name({"title": f"{name} {value}"}, upper=True) for value in values}
        self.descriptions = descriptions
        self.sub_type: Type = UnionType([LiteralType(value) for value in values])

    def depends_on(self, python_version: tuple[int, ...]) -> list["Type"]:
        """Return the needed sub types."""
        return [self.sub_type, *super().depends_on(python_version)]

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """Return the type declaration."""
        result = ["", ""]
        comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
        result.append(f"{self._name} = {self.sub_type.name(python_version)}")
        if len(comments) == 1:
            result += [f'""" {comments[0]} """']
        elif comments:
            result += ['"""', *comments, '"""']
        for value in self.values:
            name = self.value_names[value]
            formatted_value = f'"{value}"' if isinstance(value, str) else str(value)
            result.append(f"{name}: {LiteralType(value).name(python_version)} = {formatted_value}")
            name = self.descriptions[0] if self.descriptions else self._name
            name = name.removesuffix(".")
            result.append(f'"""The values for the \'{name}\' enum"""')

        result.append("")
        return result


class TypedDictType(NamedType):
    """The Type that represent a TypedDict in Python."""

    def __init__(
        self,
        name: str,
        struct: dict[str, Type],
        descriptions: list[str],
        required: set[str],
    ) -> None:
        """
        Init.

        Parameter:
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

    def depends_on(self, python_version: tuple[int, ...]) -> list[Type]:
        """Get the types that we requires to be valid."""
        result: list[Type] = [NativeType("TypedDict")]
        result += self.struct.values()
        return result + super().depends_on(python_version)

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """Get the definition based on a dict."""
        supported_re = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        # Support to be a class
        supported = True

        for property_ in self.struct:
            if not supported_re.match(property_) or property_ in keyword.kwlist:
                supported = False
                break

        result = ["", ""]
        if supported:
            result.append(f"class {self._name}(TypedDict, total=False):")
            comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
            if len(comments) == 1:
                result.append(f'    """ {comments[0]} """')
                result.append("")
            elif comments:
                result.append('    """')
                result += [f"    {d}" if d else "" for d in comments]
                result.append('    """')
                result.append("")

            for property_, type_obj in self.struct.items():
                result.append(f"    {property_}: {type_obj.name(python_version)}")
                comments = type_obj.comments()
                if len(comments) == 1:
                    result.append(f'    """ {comments[0]} """')
                    result.append("")
                elif comments:
                    result.append('    """')
                    result += [f"    {comment}" if comment else "" for comment in comments]
                    result.append('    """')
                    result.append("")
        else:
            result += [
                "# | " + d for d in split_comment(self.descriptions, line_length - 2 if line_length else None)
            ]
            result.append(f"{self._name} = TypedDict('{self._name}', " + "{")
            for property_, type_obj in self.struct.items():
                result += [f"    # | {comment}" for comment in type_obj.comments()]
                result.append(f"    '{property_}': {type_obj.name(python_version)},")
            result.append("}, total=False)")
        return result


class Constant(NamedType):
    """The Pseudo Type is used to add the default constants."""

    def __init__(self, name: str, constant: Any, descriptions: list[str]) -> None:
        """
        Init.

        Parameter:
            name: the type name
            constant: the constant value
            descriptions: the type description
        """
        super().__init__(name)
        self.constant = constant
        self.descriptions = descriptions

    def definition(self, python_version: tuple[int, ...], line_length: Optional[int] = None) -> list[str]:
        """Return the type declaration."""
        result = ["", ""]
        if isinstance(self.constant, dict) and not self.constant:
            dict_type = "Dict" if python_version < (3, 9) else "dict"
            result.append(f"{self._name}: {dict_type}[str, Any] = {self.constant!r}")
        elif isinstance(self.constant, (dict, list)) and not self.constant:
            list_type = "List" if python_version < (3, 9) else "list"
            result.append(f"{self._name}: {list_type}[Any] = {self.constant!r}")
        else:
            result.append(f"{self._name} = {self.constant!r}")
        comments = split_comment(self.descriptions, line_length - 2 if line_length else None)
        if len(comments) == 1:
            result += [f'""" {comments[0]} """', ""]
        elif comments:
            result += ['"""', *comments, '"""', ""]
        return result

    def imports(self, python_version: tuple[int, ...]) -> list[tuple[str, str]]:
        """Return the needed imports."""
        if isinstance(self.constant, dict) and not self.constant:
            if python_version < (3, 9):
                return [("typing", "Any"), ("typing", "Dict")]
            return [("typing", "Any")]
        if isinstance(self.constant, list) and not self.constant:
            if python_version < (3, 9):
                return [("typing", "Any"), ("typing", "List")]
            return [("typing", "Any")]
        return []


def split_comment(text: list[str], line_length: Optional[int]) -> list[str]:
    """
    Split the text at line length.

    Parameter:
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
    schema: Optional[
        Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
        ]
    ],
    proposed_name: Optional[str] = None,
    upper: bool = False,
    get_name_properties: Optional[str] = None,
    postfix: Optional[str] = None,
) -> str:
    """
    Get the name for an element.

    Parameter:
        schema: the concerned schema
        proposed_name: a name that we will use it the schema hasn't any title
        upper: should we use an upper case (For constants)
    """
    # Get the base name
    has_title = isinstance(schema, dict) and "title" in schema
    name = schema["title"] if has_title else proposed_name  # type: ignore[index]
    assert name is not None
    name = normalize(name)

    prefix = "" if has_title else "_"
    if upper:
        # Upper case
        name = name.upper()
        # Remove spaces
        output = prefix + "".join(["_" if char.isspace() else char for char in name])
    elif get_name_properties == "UpperFirst":
        # Change just the first letter to upper case
        name = name[0].upper() + name[1:]
        # Remove spaces
        output = prefix + "".join([char for char in name if not char.isspace()])
    else:
        # Title case
        name = name.title()
        # Remove spaces
        output = prefix + "".join([char for char in name if not char.isspace()])
    if postfix:
        output += postfix
    if not get_name.__dict__.get("names"):
        get_name.__dict__["names"] = set()
    elif output in get_name.__dict__["names"]:
        output += str(random.randint(0, 9999))  # noqa: S311 # nosec
    get_name.__dict__["names"].add(output)
    return output


def get_description(
    schema: Union[
        jsonschema_draft_04.JSONSchemaD4,
        jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
    ],
) -> list[str]:
    """
    Get the standard description for an element.

    Parameter:
        schema: the concerned schema
    """
    result: list[str] = []
    if "title" in schema:
        result.append(f"{schema['title']}.")
        schema.setdefault("used", set()).add("title")  # type: ignore[typeddict-item]
    if "description" in schema:
        schema.setdefault("used", set()).add("description")  # type: ignore[typeddict-item]
        if result:
            result.append("")
        result += schema["description"].split("\n")
    first = True
    used = cast("set[str]", schema.get("used", set()))
    used = {
        *used,
        "$schema",
        "$id",
        "type",
        "used",
        "required",
        "$defs",
        "definitions",
        "properties",
    }
    for key, value in schema.items():
        if key not in used:
            if not isinstance(value, (list, dict)):
                if first:
                    if result:
                        result.append("")
                    first = False
                result.append(f"{key}: {value}")
            else:
                if first:
                    if result:
                        result.append("")
                    first = False
                result.append(f"{key}:")
                lines = yaml.dump(value, Dumper=yaml.SafeDumper).split("\n")
                result += [f"  {line}" for line in lines if line]

    return result
