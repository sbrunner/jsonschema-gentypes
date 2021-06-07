import os
import tempfile

import ruamel.yaml
import yaml

from jsonschema_gentypes.validate import validate


def test_validate_ruamel():
    errors, data = validate(
        "test.yaml",
        ruamel.yaml.round_trip_load(
            """
root:
  - 8
  - test: 8
  - toto: 8"""
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"test": {"type": "string"}},
                        "required": ["test"],
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml:3:3 root.0: 8 is not of type 'object'",
        "-- test.yaml:4:5 root.1.test: 8 is not of type 'string'",
        "-- test.yaml:5:5 root.2: 'test' is a required property",
    ]


def test_validate_yaml():
    errors, data = validate(
        "test.yaml",
        yaml.load(
            """
root:
  - 8
  - test: 8
  - toto: 8"""
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"test": {"type": "string"}},
                        "required": ["test"],
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml root.0: 8 is not of type 'object'",
        "-- test.yaml root.1.test: 8 is not of type 'string'",
        "-- test.yaml root.2: 'test' is a required property",
    ]


def test_validate_deep():
    errors, data = validate(
        "test.yaml",
        yaml.load(
            """
root:
  level2:
    test: 8"""
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "test": {"type": "string"},
                            },
                        }
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml root.level2.test: 8 is not of type 'string'",
    ]


def test_default():
    errors, data = validate(
        "test.yaml",
        {},
        {
            "type": "object",
            "properties": {
                "root": {
                    "default": "abc",
                },
            },
        },
        default=True,
    )
    assert data == {"root": "abc"}
