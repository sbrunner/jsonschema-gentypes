import re

import pytest
from jsonschema import RefResolver

import jsonschema_gentypes


def get_types(schema):
    resolver: RefResolver = RefResolver.from_schema(schema)
    api = jsonschema_gentypes.APIv7(resolver)
    return api.get_type(schema)


def test_basic_types():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "description": "A description",
            "properties": {
                "string": {"type": "string", "title": "A string"},
                "number": {"type": "number", "description": "A number"},
                "integer": {"type": "integer", "title": "An integer", "description": "An integer"},
                "boolean": {"type": "boolean"},
                "null": {"type": "null"},
                "const": {"const": 8},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
#
# A description
TestBasicTypes = TypedDict('TestBasicTypes', {
    # A string
    'string': str,
    # A number
    'number': Union[int, float],
    # An integer
    #
    # An integer
    'integer': int,
    'boolean': bool,
    'null': None,
    'const': Literal[8],
}, total=False)"""
    )


def test_ref():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "definitions": {
                "string": {"type": "string"},
            },
            "properties": {
                "string": {"$ref": "#/definitions/string"},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    'string': str,
}, total=False)"""
    )


def test_array():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {"type": "array", "items": {"type": "string"}},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    'array': List[str],
}, total=False)"""
    )


def test_array_true():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {"type": "array", "items": True},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    'array': List[Any],
}, total=False)"""
    )


def test_array_tuple():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": [{"type": "string"}, {"type": "number"}],
                },
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    # minItems: 2
    # maxItems: 2
    'array': Tuple[str, Union[int, float]],
}, total=False)"""
    )


def test_additional_properties_mixed():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "string": {"type": "string"},
            },
            "additionalProperties": {"type": "string"},
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
#
# WARNING: The required are not correctly taken in account,
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/6
#
# WARNING: the Normally the types should be mised each other instead of Union.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
TestBasicTypes = Union[Dict[str, str], "TestBasicTypesTyped"]"""
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition()])
        == """

TestBasicTypesTyped = TypedDict('TestBasicTypesTyped', {
    'string': str,
}, total=False)"""
    )


def test_additional_properties():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "additionalProperties": {"type": "string"},
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = Dict[str, str]"""
    )


def test_additional_properties_true():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "additionalProperties": True,
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = Dict[str, Any]"""
    )


def test_boolean_const():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {"boolean": {"type": "boolean", "const": True}},
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    'boolean': Literal[True],
}, total=False)"""
    )


def test_enum():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {"enum": {"type": "string", "enum": ["red", "amber", "green"]}},
            "required": ["enum"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    'enum': "_TestBasicTypesEnum",
}, total=False)"""
    )

    assert len(type_.depends_on()) == 2
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[1].definition()])
        == '''

class _TestBasicTypesEnum(Enum):
    RED = "red"
    AMBER = "amber"
    GREEN = "green"'''
    )


def test_any_of():
    type_ = get_types(
        {
            "title": "test basic types",
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "string1": {"type": "string"},
                    },
                },
                {
                    "type": "object",
                    "properties": {
                        "string2": {"type": "string"},
                    },
                },
            ],
            "required": ["string"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = Union["_TestBasicTypesAnyof0", "_TestBasicTypesAnyof1"]"""
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition()])
        == """

_TestBasicTypesAnyof0 = TypedDict('_TestBasicTypesAnyof0', {
    'string1': str,
}, total=False)"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition()])
        == """

_TestBasicTypesAnyof1 = TypedDict('_TestBasicTypesAnyof1', {
    'string2': str,
}, total=False)"""
    )


def test_all_of() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "allOf": [
                {
                    "type": "object",
                    "properties": {
                        "string1": {"type": "string"},
                    },
                },
                {
                    "type": "object",
                    "properties": {
                        "string2": {"type": "string"},
                    },
                },
            ],
            "required": ["string"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
#
# WARNING: PEP 544 does not support an Intersection type,
# so `allOf` is interpreted as a `Union` for now.
# See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
TestBasicTypes = Union["_TestBasicTypesAllof0", "_TestBasicTypesAllof1"]"""
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition()])
        == """

_TestBasicTypesAllof0 = TypedDict('_TestBasicTypesAllof0', {
    'string1': str,
}, total=False)"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition()])
        == """

_TestBasicTypesAllof1 = TypedDict('_TestBasicTypesAllof1', {
    'string2': str,
}, total=False)"""
    )


def test_one_of() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "string1": {"type": "string"},
                    },
                },
                {
                    "type": "object",
                    "properties": {
                        "string2": {"type": "string"},
                    },
                },
            ],
            "required": ["string"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
#
# oneOf
TestBasicTypes = Union["_TestBasicTypesOneof0", "_TestBasicTypesOneof1"]"""
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition()])
        == """

_TestBasicTypesOneof0 = TypedDict('_TestBasicTypesOneof0', {
    'string1': str,
}, total=False)"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition()])
        == """

_TestBasicTypesOneof1 = TypedDict('_TestBasicTypesOneof1', {
    'string2': str,
}, total=False)"""
    )


def test_type_list() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "type": ["string", "boolean"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = Union[str, bool]"""
    )


def test_it_the_else() -> None:  # 395
    type_ = get_types(
        {
            "title": "test basic types",
            "type": "object",
            "if": {"properties": {"type": {"const": "type"}}},
            "then": {"properties": {"text1": {"type": "string"}}},
            "else": {"properties": {"text2": {"type": "string"}}},
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = Union["_TestBasicTypesThen", "_TestBasicTypesElse"]"""
    )

    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition()])
        == """

_TestBasicTypesThen = TypedDict('_TestBasicTypesThen', {
    'text1': str,
    'type': Literal["type"],
}, total=False)"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition()])
        == """

_TestBasicTypesElse = TypedDict('_TestBasicTypesElse', {
    'text2': str,
}, total=False)"""
    )


@pytest.mark.parametrize(
    "value,expected_type", [(11, "11"), (1.1, "1.1"), (True, "True"), ("test", '"test"'), (None, "None")]
)
def test_const(value, expected_type) -> None:
    type_ = get_types({"title": "test basic types", "const": value})
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == f"""

# test basic types
TestBasicTypes = Literal[{expected_type}]"""
    )


def test_enum() -> None:
    type_ = get_types({"title": "test basic types", "enum": ["red", "amber", "green"]})
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == '''

class TestBasicTypes(Enum):
    """
    test basic types.
    """
    RED = "red"
    AMBER = "amber"
    GREEN = "green"'''
    )


def test_enum_int() -> None:
    type_ = get_types({"title": "test basic types", "enum": [1, 2, 3]})
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == '''

class TestBasicTypes(Enum):
    """
    test basic types.
    """
    NUM_1 = 1
    NUM_2 = 2
    NUM_3 = 3'''
    )


def test_enum_bool() -> None:
    type_ = get_types({"title": "test basic types", "enum": [True, False]})
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == '''

class TestBasicTypes(Enum):
    """
    test basic types.
    """
    TRUE_NAME = True
    FALSE_NAME = False'''
    )


@pytest.mark.parametrize(
    "value,expected_type", [(11, "int"), (1.1, "float"), (True, "bool"), ("test", "str"), (None, "Any")]
)
def test_default(value, expected_type) -> None:
    type_ = get_types({"title": "test basic types", "default": value})
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == f"""

# test basic types
#
# default: {value}
TestBasicTypes = {expected_type}"""
    )


def test_typeddict_mixrequired():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "text1": {"type": "string"},
                "text2": {"type": "string"},
            },
            "required": ["text1"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition()])
        == """

# test basic types
TestBasicTypes = TypedDict('TestBasicTypes', {
    # required
    'text1': str,
    'text2': str,
}, total=False)"""
    )


@pytest.mark.parametrize(
    "config,title,expected",
    [
        ({"title": "test1"}, "test2", "Test1"),
        ({"title": "test"}, None, "Test"),
        (None, "test", "_Test"),
        (None, "if", "_IfName"),
        (None, "françois", "_Francois"),
        (None, "10°", "_Num10Deg"),
        (None, "a test", "_ATest"),
        (None, "義勇軍進行曲", "_YiYongJunJinXingQu"),
        (None, "éàè", "_Eae"),
    ],
)
def test_name(config, title, expected):
    assert jsonschema_gentypes.get_name(config, title) == expected


def test_name_upper():
    assert jsonschema_gentypes.get_name({"title": "test"}, upper=True) == "TEST"
