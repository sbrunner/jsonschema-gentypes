from typing import Any, Optional

import pytest

import jsonschema_gentypes.api_draft_07
import jsonschema_gentypes.api_draft_2019_09
import jsonschema_gentypes.api_draft_2020_12
import jsonschema_gentypes.resolver
from jsonschema_gentypes.api import Type

from .test_test import get_types


def get_definition(type_: Type) -> list[str]:
    """Get the type full definition"""
    actual = []
    actual += [e for e in type_.definition(None) if e]

    for t_ in type_.depends_on():
        sub_definition = get_definition(t_)
        if sub_definition:
            if actual:
                actual.append("")
            actual += sub_definition
    return actual


def assert_expected(type_: Type, expected: list[str], path: Optional[list[int]] = None) -> None:
    """Assert that the full definition is correct"""
    if path is None:
        path = []

    assert get_definition(type_) == expected


@pytest.mark.parametrize(  # type: ignore[misc]
    "first, second, third, expected",
    [
        [
            "anyOf",
            "anyOf",
            "anyOf",
            [
                '_Base = Union["_BaseAnyof0", Union["_BaseAnyofAnyof0", '
                'Union["_BaseAnyofAnyofAnyof0", "_BaseAnyofAnyofAnyof1"]]]',
                '""" Aggregation type: anyOf """',
                "",
                "class _BaseAnyof0(TypedDict, total=False):",
                "    p1: str",
                "",
                "class _BaseAnyofAnyof0(TypedDict, total=False):",
                "    p2: str",
                "",
                "class _BaseAnyofAnyofAnyof0(TypedDict, total=False):",
                "    p3: str",
                "",
                "class _BaseAnyofAnyofAnyof1(TypedDict, total=False):",
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "anyOf",
            "allOf",
            [
                '_Base = Union["_BaseAnyof0", Union["_BaseAnyofAnyof0", ' '"_BaseAnyofAnyof"]]',
                '""" Aggregation type: anyOf """',
                "",
                "class _BaseAnyof0(TypedDict, total=False):",
                "    p1: str",
                "",
                "class _BaseAnyofAnyof0(TypedDict, total=False):",
                "    p2: str",
                "",
                "class _BaseAnyofAnyof(TypedDict, total=False):",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "allOf",
            "anyOf",
            [
                '_Base = Union["_BaseAnyof0", "_BaseAnyof"]',
                '""" Aggregation type: anyOf """',
                "",
                "class _BaseAnyof0(TypedDict, total=False):",
                "    p1: str",
                "",
                "class _BaseAnyof(TypedDict, total=False):",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "allOf",
            "allOf",
            [
                '_Base = Union["_BaseAnyof0", "_BaseAnyof"]',
                '""" Aggregation type: anyOf """',
                "",
                "class _BaseAnyof0(TypedDict, total=False):",
                "    p1: str",
                "",
                "class _BaseAnyof(TypedDict, total=False):",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "anyOf",
            "anyOf",
            [
                "class _Base(TypedDict, total=False):",
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "anyOf",
            "allOf",
            [
                "class _Base(TypedDict, total=False):",
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "allOf",
            "anyOf",
            [
                "class _Base(TypedDict, total=False):",
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "allOf",
            "allOf",
            [
                "class _Base(TypedDict, total=False):",
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
            ],
        ],
    ],
)
def test_combining(first: str, second: str, third: str, expected: Any) -> None:
    type_ = get_types(
        {
            "type": "object",
            first: [
                {
                    "properties": {
                        "p1": {"type": "string"},
                    },
                },
                {
                    second: [
                        {
                            "properties": {
                                "p2": {"type": "string"},
                            }
                        },
                        {
                            third: [
                                {
                                    "properties": {
                                        "p3": {"type": "string"},
                                    },
                                },
                                {
                                    "properties": {
                                        "p4": {"type": "string"},
                                    },
                                },
                            ]
                        },
                    ],
                },
            ],
        }
    )
    assert_expected(type_, expected)


@pytest.mark.parametrize(  # type: ignore[misc]
    "first, second, third, expected",
    [
        [
            "anyOf",
            "anyOf",
            "anyOf",
            [
                'Combined = Union["P1", Union["P2", Union["P3", "P4"]]]',
                '"""',
                "combined.",
                "Aggregation type: anyOf",
                'Subtype: "P1", "P2", "P3", "P4"',
                '"""',
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "anyOf",
            "allOf",
            [
                'Combined = Union["P1", Union["P2", "_CombinedAnyofAnyof"]]',
                '"""',
                "combined.",
                "Aggregation type: anyOf",
                'Subtype: "P1", "P2", "P3", "P4"',
                '"""',
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class _CombinedAnyofAnyof(TypedDict, total=False):",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "allOf",
            "anyOf",
            [
                'Combined = Union["P1", "_CombinedAnyof"]',
                '"""',
                "combined.",
                "Aggregation type: anyOf",
                'Subtype: "P1", "P2", "P3", "P4"',
                '"""',
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class _CombinedAnyof(TypedDict, total=False):",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "anyOf",
            "allOf",
            "allOf",
            [
                'Combined = Union["P1", "_CombinedAnyof"]',
                '"""',
                "combined.",
                "Aggregation type: anyOf",
                'Subtype: "P1", "P2", "P3", "P4"',
                '"""',
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class _CombinedAnyof(TypedDict, total=False):",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "anyOf",
            "anyOf",
            [
                "class Combined(TypedDict, total=False):",
                '    """ combined. """',
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "anyOf",
            "allOf",
            [
                "class Combined(TypedDict, total=False):",
                '    """ combined. """',
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "allOf",
            "anyOf",
            [
                "class Combined(TypedDict, total=False):",
                '    """ combined. """',
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
        [
            "allOf",
            "allOf",
            "allOf",
            [
                "class Combined(TypedDict, total=False):",
                '    """ combined. """',
                "    p1: str",
                "    p2: str",
                "    p3: str",
                "    p4: str",
                "",
                "class P1(TypedDict, total=False):",
                '    """ p1. """',
                "    p1: str",
                "",
                "class P2(TypedDict, total=False):",
                '    """ p2. """',
                "    p2: str",
                "",
                "class P3(TypedDict, total=False):",
                '    """ p3. """',
                "    p3: str",
                "",
                "class P4(TypedDict, total=False):",
                '    """ p4. """',
                "    p4: str",
            ],
        ],
    ],
)
def test_combining_title(first: str, second: str, third: str, expected: Any) -> None:
    type_ = get_types(
        {
            "title": "combined",
            "type": "object",
            first: [
                {
                    "title": "p1",
                    "properties": {
                        "p1": {"type": "string"},
                    },
                },
                {
                    second: [
                        {
                            "title": "p2",
                            "properties": {
                                "p2": {"type": "string"},
                            },
                        },
                        {
                            third: [
                                {
                                    "title": "p3",
                                    "properties": {
                                        "p3": {"type": "string"},
                                    },
                                },
                                {
                                    "title": "p4",
                                    "properties": {
                                        "p4": {"type": "string"},
                                    },
                                },
                            ]
                        },
                    ],
                },
            ],
        }
    )
    assert_expected(type_, expected)
