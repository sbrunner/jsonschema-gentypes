# JSON Schema generate Python types

kk
Tools to generate Python types based on TypedDict from a JSON schema

## Quick start

install:

```bash
python3 -m pip install --user jsonschema-gentypes
```

Convert a JSON schema to a Python file contains the types:

```bash
jsonschema-gentypes --json-schema=<JSON schema> --python=<destination Python file>
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
    # The minimum Python version that the code should support. By default the
    # currently executing Python version is chosen. Note that the output
    # may require typing_extensions to be installed.
    python_version: '3.11'
```

And just run:

```bash
jsonschema-gentypes
```

## Default

The default values are exported in the Python file, then you can do something like that:

```python
value_with_default = my_object.get('field_name', my_schema.FIELD_DEFAULT)
```

## Limitations

Requires Python 3.8

See the [issues with label "limitation"](https://github.com/camptocamp/jsonschema-gentypes/issues?q=is%3Aissue+is%3Aopen+label%3Alimitation).

## Pre-commit hooks

This project provides pre-commit hooks to automatically generate the files.

```yaml
repos:
  - repo: https://github.com/camptocamp/jsonschema-gentypes
    rev: <version> # Use the ref you want to point at
    hools:
      - id: jsonschema-gentypes
        files: |
          (?x)^(
              jsonschema-gentypes\.yaml|
              <schema_path>\.json
          )$
```

See also the pre_commit section in the configuration to run the pre-commit just after the generation, for example with:

```yaml
pre_commit:
  enabled: true
  arguments:
    - --color=never
```

## OpenAPI3

We can also generate types for OpenAPI3 schemas (automatically detected).

The result of our example in `tests/openapi3.json` can be used in pyramid with for example:

```python
import pyramid.request
from pyramid.view import view_config
from openaoi3 import *

def open_api(func):
    def wrapper(request: pyramid.request.Request, **kwargs) -> Any:
        typed_request = {}
        try:
            typed_request{'request_body'} = request.json
        except Exception as e:
            pass
        typed_request{'path'} = request.matchdict
        typed_request{'query'} = request.params

        return = func(request, request_typed=typed_request, **kwargs)

    return wrapper


@view_config(route_name="route_name", renderer="json")
@open_api
def view(
  request: pyramid.request.Request,
  request_typed: OgcapiCollectionsCollectionidGet,
) -> OgcapiCollectionsCollectionidGetResponse:
    return {...}
```

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

The `prospector` tests should pass.

The code should be typed.

The code should be tested with `pytests`.
