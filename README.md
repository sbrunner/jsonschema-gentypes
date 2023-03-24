# JSON Schema generate Python types

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

## Validation

This package also provide some validations features for YAML file based on `jsonschema`.

Additional features:

- Obtain the line and columns number in the errors, if the file is loaded with `ruamel.yaml`.
- Export the default provided in the JSON schema.

```python
    import ruamel.yaml
    import pkgutil
    import jsonschema_gentypes.validate

    schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")
    with open(filename) as data_file:
        yaml = ruamel.yaml.YAML()  # type: ignore
        data = yaml.load(data_file)
    errors, data = jsonschema_gentypes.validate.validate(filename, data, schema)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
```

The filling of the default value is deprecated because it can produce quite peculiar things, see also
[the jsonschema documentation](https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance).

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

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

The `prospector` tests should pass.

The code should be typed.

The code should be tested with `pytests`.
