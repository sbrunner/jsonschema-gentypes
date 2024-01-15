import pytest

import jsonschema_gentypes.api_draft_07
import jsonschema_gentypes.api_draft_2019_09
import jsonschema_gentypes.api_draft_2020_12
import jsonschema_gentypes.resolver


def get_types(schema):
    resolver = jsonschema_gentypes.resolver.RefResolver("https://example.com/fake", schema)
    api = jsonschema_gentypes.api_draft_07.APIv7(resolver)
    return api.get_type(schema, "Base")


def get_types_2019_09(schema):
    resolver = jsonschema_gentypes.resolver.RefResolver("https://example.com/fake", schema)
    api = jsonschema_gentypes.api_draft_2019_09.APIv201909(resolver)
    return api.get_type(schema, "Base")


def get_types_2020_12(schema):
    resolver = jsonschema_gentypes.resolver.RefResolver("https://example.com/fake", schema)
    api = jsonschema_gentypes.api_draft_2020_12.APIv202012(resolver)
    return api.get_type(schema, "Base")


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
                "string_required": {"type": "string", "title": "A string"},
                "number_required": {"type": "number", "description": "A number"},
                "integer_required": {"type": "integer", "title": "An integer", "description": "An integer"},
                "boolean": {"type": "boolean"},
                "null": {"type": "null"},
                "const": {"const": 8},
                "true": True,
                "false": False,
            },
            "required": ["string_required", "number_required", "integer_required"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """
    test basic types.

    A description
    """

    string: str
    """ A string. """

    number: Union[int, float]
    """ A number """

    integer: int
    """
    An integer.

    An integer
    """

    boolean: bool
    string_required: Required[str]
    """
    A string.

    Required property
    """

    number_required: Required[Union[int, float]]
    """
    A number

    Required property
    """

    integer_required: Required[int]
    """
    An integer.

    An integer

    Required property
    """

    null: None
    const: Literal[8]
    true: Any
    false: None'''
    )


def test_dict_style():
    type_ = get_types(
        {
            "type": "object",
            "properties": {
                "123": {"type": "string"},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == """

_Base = TypedDict('_Base', {
    '123': str,
}, total=False)"""
    )


def test_ref():
    type_ = get_types(
        {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.com/fake",
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    string: str'''
    )


def test_self_ref():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "definitions": {
                "string": {"type": "string"},
            },
            "properties": {
                "string": {"$ref": "#"},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    string: "TestBasicTypes"
    """ test basic types. """
'''
    )


def test_recursive_ref():
    type_ = get_types_2019_09(
        {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.com/tree",
            "$recursiveAnchor": True,
            "title": "Ref1",
            "type": "object",
            "properties": {
                "data": {
                    "title": "Ref2",
                    "type": "object",
                    "$recursiveAnchor": True,
                    "properties": {"data_child": {"$recursiveRef": "#"}},
                },
                "children": {"type": "array", "items": {"$recursiveRef": "#"}},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class Ref1(TypedDict, total=False):
    """ Ref1. """

    data: "Ref2"
    children: List["Ref1"]'''
    )
    depends_on = [e for e in type_.depends_on() if e.definition(None)]
    assert len(depends_on) == 1
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[1].definition(None)])
        == '''

class Ref2(TypedDict, total=False):
    """ Ref2. """

    data_child: "Ref2"'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: List[str]'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: List[Any]'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: Tuple[str, Union[int, float]]
    """
    minItems: 2
    maxItems: 2
    """
'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union[Dict[str, str], "TestBasicTypesTyped"]
"""
test basic types.


WARNING: Normally the types should be a mix of each other instead of Union.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
"""
'''
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition(None)])
        == f"""

class TestBasicTypesTyped(TypedDict, total=False):
    string: str"""
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Dict[str, str]
""" test basic types. """
'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Dict[str, Any]
""" test basic types. """
'''
    )


def test_pattern_properties_multiple():
    type_ = get_types(
        {
            "type": "object",
            "title": "Pattern properties with tow patterns",
            "patternProperties": {"^[a-z]+$": {"type": "string"}, "^[0-9]+$": {"type": "number"}},
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

PatternPropertiesWithTowPatterns = Dict[str, Any]
"""
Pattern properties with tow patterns.

patternProperties:
  ^[0-9]+$:
    type: number
  ^[a-z]+$:
    type: string
"""
'''
    )


def test_pattern_properties_string():
    type_ = get_types(
        {
            "type": "object",
            "title": "Pattern properties with one pattern as string",
            "patternProperties": {
                "^[a-z]+$": {"type": "string"},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

PatternPropertiesWithOnePatternAsString = Dict[str, str]
""" Pattern properties with one pattern as string. """
'''
    )


def test_pattern_properties_object():
    type_ = get_types(
        {
            "type": "object",
            "title": "Pattern properties with one pattern as object",
            "patternProperties": {
                "^[a-z]+$": {
                    "type": "object",
                    "properties": {
                        "prop": {"type": "string"},
                    },
                },
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

PatternPropertiesWithOnePatternAsObject = Dict[str, "_PatternPropertiesWithOnePatternAsObjectType"]
""" Pattern properties with one pattern as object. """
'''
    )

    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition(None)])
        == f"""

class _PatternPropertiesWithOnePatternAsObjectType(TypedDict, total=False):
    prop: str"""
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    boolean: Literal[True]'''
    )


def test_enum():
    type_ = get_types(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "enum": {"title": "properties", "type": "string", "enum": ["red", "amber", "green"]}
            },
            "required": ["enum"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

"""
test basic types.
"""
TestBasicTypes = TypedDict('TestBasicTypes', {
    'enum': "_TestBasicTypesEnum",
}, total=False) """
'''
    )

    assert len(type_.depends_on()) == 2
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[1].definition(None)])
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union["_TestBasicTypesAnyof0", "_TestBasicTypesAnyof1"]
"""
test basic types.

Aggregation type: anyOf
"""
'''
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition(None)])
        == f"""

class _TestBasicTypesAnyof0(TypedDict, total=False):
    string1: str"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition(None)])
        == f"""

class _TestBasicTypesAnyof1(TypedDict, total=False):
    string2: str"""
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    string1: str
    string2: str'''
    )


def test_all_of_2() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "allOf": [{"type": "string"}, {"type": "number"}],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = None
""" test basic types. """
'''
    )


def test_all_of_3() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "allOf": [{"type": "string"}, {"maxLength": 5}],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = str
"""
test basic types.

maxLength: 5
"""
'''
    )


def test_all_of_4() -> None:
    type_ = get_types(
        {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.com/fake",
            "type": "object",
            "title": "test basic types",
            "definitions": {
                "nonNegativeInteger": {"type": "integer", "minimum": 0},
            },
            "properties": {
                "test": {"allOf": [{"$ref": "#/definitions/nonNegativeInteger"}, {"default": 0}]},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    test: "_TestBasicTypesTest"
    """
    minimum: 0
    default: 0
    """
'''
    )
    assert len(type_.depends_on()) == 2
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[1].definition(None)])
        == '''

_TestBasicTypesTest = int
"""
minimum: 0
default: 0
"""
'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union["_TestBasicTypesOneof0", "_TestBasicTypesOneof1"]
"""
test basic types.

Aggregation type: oneOf
"""
'''
    )
    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition(None)])
        == f"""

class _TestBasicTypesOneof0(TypedDict, total=False):
    string1: str"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition(None)])
        == f"""

class _TestBasicTypesOneof1(TypedDict, total=False):
    string2: str"""
    )


def test_type_list() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "type": ["string", "boolean"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union[str, bool]
""" test basic types. """
'''
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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union["_TestBasicTypesThen", "_TestBasicTypesElse"]
""" test basic types. """
'''
    )

    assert len(type_.depends_on()) == 1
    assert len(type_.depends_on()[0].depends_on()) == 3
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[1].definition(None)])
        == f"""

class _TestBasicTypesThen(TypedDict, total=False):
    text1: str
    type: Literal['type']"""
    )
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].depends_on()[2].definition(None)])
        == f"""

class _TestBasicTypesElse(TypedDict, total=False):
    text2: str"""
    )


@pytest.mark.parametrize(
    "value,expected_type", [(11, "11"), (1.1, "1.1"), (True, "True"), ("test", "'test'"), (None, "None")]
)
def test_const(value, expected_type) -> None:
    type_ = get_types({"title": "test basic types", "const": value})
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Literal[{expected_type}]
""" test basic types. """
'''
    )


def test_enum() -> None:
    type_ = get_types({"title": "test basic types", "enum": ["red", "amber", "green"]})

    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

TestBasicTypes = Union[Literal['red'], Literal['amber'], Literal['green']]
""" test basic types. """
TESTBASICTYPES_RED: Literal['red'] = "red"
"""The values for the 'test basic types' enum"""
TESTBASICTYPES_AMBER: Literal['amber'] = "amber"
"""The values for the 'test basic types' enum"""
TESTBASICTYPES_GREEN: Literal['green'] = "green"
"""The values for the 'test basic types' enum"""
'''
    )


def test_enum_int() -> None:
    type_ = get_types({"title": "test basic types", "enum": [1, 2, 3]})
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union[Literal[1], Literal[2], Literal[3]]
""" test basic types. """
TESTBASICTYPES_1: Literal[1] = 1
"""The values for the 'test basic types' enum"""
TESTBASICTYPES_2: Literal[2] = 2
"""The values for the 'test basic types' enum"""
TESTBASICTYPES_3: Literal[3] = 3
"""The values for the 'test basic types' enum"""
'''
    )


def test_enum_bool() -> None:
    type_ = get_types({"title": "test basic types", "enum": [True, False]})
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Union[Literal[True], Literal[False]]
""" test basic types. """
TESTBASICTYPES_TRUE: Literal[True] = True
"""The values for the 'test basic types' enum"""
TESTBASICTYPES_FALSE: Literal[False] = False
"""The values for the 'test basic types' enum"""
'''
    )


@pytest.mark.parametrize(
    "value,expected_type", [(11, "int"), (1.1, "float"), (True, "bool"), ("test", "str"), (None, "Any")]
)
def test_default(value, expected_type) -> None:
    type_ = get_types({"title": "test basic types", "default": value})
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[0].definition(None)])
        == f'''

"""
test basic types.

default: {value}
TestBasicTypes = {expected_type} """
'''
    )


@pytest.mark.parametrize(
    "value,expected_type,import_",
    [
        (11, " = 11", []),
        (1.1, " = 1.1", []),
        (True, " = True", []),
        ("test", " = 'test'", []),
        (None, " = None", []),
        ([111], " = [111]", []),
        ({"aa": 111}, " = {'aa': 111}", []),
        ([], ": List[Any] = []", [("typing", "Any"), ("typing", "List")]),
        ({}, ": Dict[str, Any] = {}", [("typing", "Any"), ("typing", "Dict")]),
    ],
)
def test_default(value, expected_type, import_) -> None:
    type_ = get_types({"title": "test basic types", "type": "string", "default": value}).depends_on()[-1]
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TEST_BASIC_TYPES_DEFAULT{expected_type}
""" Default value of the field path 'Base' """
'''
    )
    assert type_.imports(None) == import_


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
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    text1: Required[str]
    """ Required property """

    text2: str'''
    )


def test_multiline() -> None:
    type_ = get_types({"title": "test basic types", "description": "first\nsecond", "const": 111})
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == f'''

TestBasicTypes = Literal[111]
"""
test basic types.

first
second
"""
'''
    )


def test_linesplit() -> None:
    type_ = get_types(
        {
            "title": "test basic types",
            "description": "The JSON Schema project intends to shepherd all three draft series to either: RFC status, the equivalent within another standards body, and/or join a foundation and establish self publication rules.",
            "const": 111,
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(line_length=80)])
        == f'''

TestBasicTypes = Literal[111]
"""
test basic types.

The JSON Schema project intends to shepherd all three draft series to either:
RFC status, the equivalent within another standards body, and/or join a
foundation and establish self publication rules.
"""
'''
    )


@pytest.mark.parametrize(
    "config,title,expected",
    [
        ({"title": "test1"}, "test2", "Test1"),
        ({"title": "test"}, None, "Test"),
        (None, "test", "_Test"),
        (None, "if", "_IfName"),
        (None, "30\U0001d5c4\U0001d5c6/\U0001d5c1", "_Num30KmSolidusH"),
        (None, "30km/h", "_Num30KmSolidusH"),
        (None, "10°", "_Num10Degree"),
        (None, "a test", "_ATest"),
        (None, "a-test", "_ATest"),
        (None, "a\ttest", "_ATest"),
        (None, "a\ntest", "_ATest"),
        (None, "éàè", "_Eae"),
        (None, "françois", "_Francois"),
        (None, "kožušček", "_Kozuscek"),
        (None, "Málagueña", "_Malaguena"),
        (None, "義勇軍進行曲", "_YiYongJunJinXingQu"),
        (None, "すべての人間", "_SuhetenoRenJian"),
        (None, "Ελευθέριος Βενιζέλος", "_EleytheriosVenizelos"),
        (None, "المملكة", "_"),
    ],
)
def test_name(config, title, expected):
    assert jsonschema_gentypes.get_name(config, title) == expected


def test_name_upper():
    assert jsonschema_gentypes.get_name({"title": "test"}, upper=True) == "TEST"


def test_recursive_ref():
    type_ = get_types_2020_12(
        {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": "https://example.com/tree",
            "$dynamicAnchor": "r1",
            "title": "Ref1",
            "type": "object",
            "properties": {
                "data": {
                    "title": "Ref2",
                    "type": "object",
                    "$dynamicAnchor": "r2",
                    "properties": {"data_child": {"$dynamicRef": "#r2"}},
                },
                "children": {"type": "array", "items": {"$dynamicRef": "#r1"}},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class Ref1(TypedDict, total=False):
    """ Ref1. """

    data: "Ref2"
    """ Ref2. """

    children: List["Ref1"]'''
    )
    depends_on = [e for e in type_.depends_on() if e.definition(None)]
    assert len(depends_on) == 1
    assert (
        "\n".join([d.rstrip() for d in type_.depends_on()[1].definition(None)])
        == '''

class Ref2(TypedDict, total=False):
    """ Ref2. """

    data_child: "Ref2"
    """ Ref2. """
'''
    )


def test_array():
    type_ = get_types_2020_12(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {"type": "array", "items": {"type": "string"}},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: List[str]'''
    )


def test_array_true():
    type_ = get_types_2020_12(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {"type": "array", "items": True},
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: List[Any]'''
    )


def test_array_tuple():
    type_ = get_types_2020_12(
        {
            "type": "object",
            "title": "test basic types",
            "properties": {
                "array": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "prefixItems": [{"type": "string"}, {"type": "number"}],
                },
            },
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class TestBasicTypes(TypedDict, total=False):
    """ test basic types. """

    array: Tuple[str, Union[int, float]]
    """
    minItems: 2
    maxItems: 2
    """
'''
    )


def test_no_type():
    type_ = get_types(
        {
            "title": "my type",
            "properties": {"foo": {"type": "string"}},
            "required": ["foo"],
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

MyType = Union[str, Union[int, float], "_MyTypeObject", List[Any], bool, None]
""" my type. """
'''
    )

    assert len(type_.depends_on()) == 1
    depends_on = [e for e in type_.depends_on()[0].depends_on() if e.definition(None)]
    assert len(depends_on) == 1
    assert (
        "\n".join([d.rstrip() for d in depends_on[0].definition(None)])
        == '''

class _MyTypeObject(TypedDict, total=False):
    foo: Required[str]
    """ Required property """
'''
    )


def test_empty_array():
    type_ = get_types(
        {
            "title": "my type",
            "type": "array",
        }
    )
    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

MyType = List[Any]
""" my type. """
'''
    )
