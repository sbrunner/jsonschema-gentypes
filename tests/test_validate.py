from jsonschema_gentypes.validate import validate_error


def test_errors():
    errors, data = validate_error(
        "test.yaml",
        """
root:
  - 8
  - test: 8
  - toto: 8""",
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
