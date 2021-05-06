# JSON Schema generate Python types

Tools to generate Python types based on TypeDict from a JSON schema

## Quick start

install:

```bash
python3 -m pip install --user jsonschema-gentype
```

Convert a JSON schema to a Python file contains the types:

```bash
jsonschema-gentype --json-schema=<JSON schema> --python=<destination Python>
```

## Docker

You can also run it with Docker:

```bash
docker run --rm --user=$(id --user) --volume=$(pwd):/src camptocamp/jsonschema-gentypes
```

## Config file

You can also write a config file named `jsonschema-gentypes.yaml` with:

```yaml
headers: >
    # Automatically generated file from a JSON schema
# Used to correctly format the generated file
callbacks:
    - - black
    - - isort
generate:
    - # JSON schema file path
      source: jsonschema_gentypes/schema.json
      # Python file path
      destination: jsonschema_gentypes/configuration.py
      # The name of the root element
      root_name: Config
      # Argument passed to the API
      api_arguments:
          additional_properties: Only explicit
      # Rename an element
      name_mapping: {}
```

And just run:

```bash
jsonschema-gentype
```

## Limitations

Requires Python 3.8

See the [issues with label "limitation"](https://github.com/camptocamp/jsonschema-gentypes/issues?q=is%3Aissue+is%3Aopen+label%3Alimitation).

## Contribute

The code should be formatted with `isort` and `black`.

The code should be typed.

The `prospector` tests should pass.

The code should be tested with `pytests`.
