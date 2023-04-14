"""
Generate the type structure based on the Type class from the JSON schema file.
"""

import keyword
import re
import textwrap
import unicodedata
from typing import Any, Dict, List, Optional, Set, Tuple, Union, cast

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


class TypeProxy(Type):
    """
    A proxy on a type that can be set later.
    """

    _type: Optional[Type] = None

    def name(self) -> str:
        """
        Return what we need to use the type.
        """
        assert self._type is not None
        return self._type.name()

    def imports(self, python_version: Tuple[int, ...]) -> List[Tuple[str, str]]:
        """
        Return the needed imports.
        """
        assert self._type is not None
        return self._type.imports(python_version)

    def definition(self, line_length: Optional[int] = None) -> List[str]:
        """
        Return the type declaration.

        Arguments:
            line_length: the maximum line length
        """
        assert self._type is not None
        return self._type.definition()

    def depends_on(self) -> List["Type"]:
        """
        Return the needed sub types.
        """
        assert self._type is not None
        return self._type.depends_on()

    def add_depends_on(self, depends_on: "Type") -> None:
        """
        Add a sub type.
        """
        raise NotImplementedError

    def comments(self) -> List[str]:
        """
        Additional comments shared by the type.
        """
        return self._type.comments() if self._type is not None else []

    def set_comments(self, comments: List[str]) -> None:
        """
        Set comment on the type.
        """
        print(f"Warning: set_comments on a TypeProxy, lost comments: {comments}")

    def set_type(self, type_: Type) -> None:
        """
        Set the type.
        """
        self._type = type_


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
            result += [f'""" {comments[0]} """', ""]
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
            result += [f'""" {comments[0]} """']
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
                result.append(f'    """ {comments[0]} """')
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
                    result.append(f'    """ {comments[0]} """')
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
            result += [f'""" {comments[0]} """', ""]
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
    schema: Optional[
        Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
        ]
    ],
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


def get_description(
    schema: Union[
        jsonschema_draft_04.JSONSchemaD4,
        jsonschema_draft_2019_09_meta_data.JSONSchemaItemD2019,
    ]
) -> List[str]:
    """
    Get the standard description for an element.

    Arguments:
        schema: the concerned schema
    """
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
            lines = yaml.dump(value, Dumper=yaml.SafeDumper).split("\n")
            result += [f"  {line}" for line in lines if line]

    return result
