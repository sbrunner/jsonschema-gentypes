"""
Automatically generated file from a JSON schema.
"""

from typing import TypedDict


class T1(TypedDict, total=False):
    r"""t1."""

    t1: bool


class T2(TypedDict, total=False):
    r"""t2."""

    t2: bool


class T3(TypedDict, total=False):
    r"""t3."""

    t3: bool


class T4(TypedDict, total=False):
    r"""t4."""

    t4: bool


class T5(TypedDict, total=False):
    r"""t5."""

    t5: bool


class TestCombiningAllofAndAnyof(TypedDict, total=False):
    r"""Test combining allOf and anyOf."""

    withTitle: "Withtitle"
    r"""
    withTitle.
    Subtype: "T1", "T2", "T3", "T4", "T5"
    """

    withoutTitle: "_TestCombiningAllofAndAnyofWithouttitle"


class Withtitle(TypedDict, total=False):
    r"""withTitle."""

    t1: bool
    t2: bool
    t3: bool
    t4: bool
    t5: bool


class _TestCombiningAllofAndAnyofWithouttitle(TypedDict, total=False):
    p1: bool
    p2: bool
    p3: bool
    p4: bool
    p5: bool
