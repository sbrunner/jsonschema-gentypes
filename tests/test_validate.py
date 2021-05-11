import os
import tempfile

import ruamel.yaml
import yaml

from jsonschema_gentypes.validate import load, validate


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
        " - test.yaml:3:3 (root.0): 8 is not of type 'object' (rule: properties.root.items.type)",
        " - test.yaml:4:5 (root.1.test): 8 is not of type 'string' (rule: properties.root.items.properties.test.type)",
        " - test.yaml:5:5 (root.2): 'test' is a required property (rule: properties.root.items.required)",
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
        " - test.yaml (root.0): 8 is not of type 'object' (rule: properties.root.items.type)",
        " - test.yaml (root.1.test): 8 is not of type 'string' (rule: properties.root.items.properties.test.type)",
        " - test.yaml (root.2): 'test' is a required property (rule: properties.root.items.required)",
    ]


def test_load_default():
    yaml_file = tempfile.NamedTemporaryFile(delete=False)
    yaml_file.write("{}".encode())
    yaml_file.close()
    data = load(
        yaml_file.name,
        {
            "type": "object",
            "properties": {
                "root": {
                    "default": "abc",
                },
            },
        },
    )
    assert dict(data) == {"root": "abc"}
    os.unlink(yaml_file.name)
