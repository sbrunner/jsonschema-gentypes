"""
Module that offer some useful functions to validate the data against a JSON schema.
"""

import argparse
import json
import logging
import re
import sys
from typing import Any, Dict, Iterator, List, Optional, Tuple
from warnings import warn

import jsonschema
import requests
import ruamel.yaml
import urlparse

import jsonschema_gentypes.jsonschema

LOG = logging.getLogger(__name__)


def _extend_with_default(
    validator_class: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
) -> "jsonschema.validators._DefaultTypesDeprecatingMetaClass":
    """
    Add the default provider.

    Extends the jsonschema validator by adding a validator that fill the missing value with the default
    provided by the JSON schema.

    Arguments:
        validator_class: The validator class to be patched
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(
        validator: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
        properties: Dict[str, jsonschema_gentypes.jsonschema.JSONSchemaItem],
        instance: Optional[Dict[str, Any]],
        schema: jsonschema_gentypes.jsonschema.JSONSchemaItem,
    ) -> Iterator[jsonschema.exceptions.ValidationError]:
        """
        Set the default from the JSON schema to the data.

        Arguments:
            validator: The validator class
            properties: The properties
            instance: The data class
            schema: The full schema
        """
        for prop, subschema in properties.items():
            if "$ref" in subschema:
                ref = subschema["$ref"]
                resolve = getattr(validator.resolver, "resolve", None)
                if resolve is None:
                    with validator.resolver.resolving(ref) as resolved:
                        yield from validator.descend(instance, resolved)
                else:
                    _, resolved = validator.resolver.resolve(ref)
                    subschema = dict(subschema)  # type: ignore
                    subschema.update(resolved)
            if "default" in subschema and instance is not None:
                instance.setdefault(prop, subschema["default"])

        yield from validate_properties(
            validator,
            properties,
            instance,
            schema,
        )

    return jsonschema.validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def validate(
    filename: str, data: Dict[str, Any], schema: Dict[str, Any], default: bool = False
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Validate the YAML, with it's JSON schema.

    Arguments:
        filename: Name used to generate the error messages
        data: The data structure to be validated (should be loaded with ruamel.yaml to have the lines numbers)
        schema: The loaded JSON schema
        default: If true, fill the data with the defaults provided in the JSON schema, not working as expected
            with AnyOf and OneOf
    """
    schema_ref = schema.get("$schema", "default")
    schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
    Validator = {  # pylint: disable=invalid-name
        "draft-04": jsonschema.Draft4Validator,
        "draft-06": jsonschema.Draft6Validator,
        "draft-07": jsonschema.Draft7Validator,
    }.get(
        schema_match.group(1) if schema_match else "default",
        jsonschema.Draft7Validator,
    )
    if default:
        warn(
            "This is deprecated, use `obj.get('field', schema.FIELD_TYPE_DEFAULT)` instead.",
            DeprecationWarning,
        )
        Validator = _extend_with_default(Validator)

    validator = Validator(schema)

    def format_error(error: jsonschema.exceptions.ValidationError) -> List[str]:
        position = filename

        if hasattr(error.instance, "lc"):
            position = f"{filename}:{error.instance.lc.line + 1}:{error.instance.lc.col + 1}"
        else:
            curent_data = data
            parent = None
            if hasattr(curent_data, "lc"):
                parent = curent_data
            for path in error.absolute_path:
                curent_data = curent_data[path]
                if hasattr(curent_data, "lc"):
                    parent = curent_data
            if parent is not None:
                position = f"{filename}:{parent.lc.line + 1}:{parent.lc.col + 1}"  # type: ignore

        if error.context:
            results = []
            for context in error.context:
                results += format_error(context)
            return results
        else:
            rule = (
                f" (rule: {'.'.join([str(i) for i in error.absolute_schema_path])})"
                if error.absolute_schema_path
                else ""
            )
            return [
                f"-- {position} "
                f'{".".join([str(i) for i in error.absolute_path] if error.absolute_path else "/")}: '
                f"{error.message}{rule}"
            ]

    results = []
    for error in validator.iter_errors(data):
        results += format_error(error)
    return sorted(results), data


class ValidationError(Exception):
    """
    Exception thrown on validation issue.
    """

    def __init__(self, message: str, data: Any) -> None:
        """
        Construct.

        Arguments:
            message: The error message
            data: The validated data
        """
        super().__init__(message)
        self.data = data


def main() -> None:
    """
    Check the JSON ort YAML files against the JSON schema files.
    """
    argparser = argparse.ArgumentParser("Check the JSON ort YAML files against the JSON schema files")
    argparser.add_argument("--schema", help="The JSON schema")
    argparser.add_argument("--json", action="store_true", help="Parse as JSON")
    argparser.add_argument("--yaml", action="store_true", help="Parse as YAML")
    argparser.add_argument("--timeout", default=30, type=int, help="Timeout in seconds")
    argparser.add_argument("files", nargs="+", help="The files to check")
    args = argparser.parse_args()

    if args.json and args.yaml:
        print("You can not specify both --json and --yaml")
        sys.exit(1)

    re_ = re.compile(r".*schema=(\S+)")
    yaml = ruamel.yaml.YAML()

    for file in args.files:
        is_json = args.json
        is_yaml = args.yaml
        if not is_json and not is_yaml:
            is_json = args.file.endswith(".json")
            is_yaml = args.file.endswith(".yaml") or args.file.endswith(".yml")

        if not is_json and not is_yaml:
            print(f"Unknown file type: {file}")
            sys.exit(1)

        schema = args.schema

        if schema is None and is_yaml:
            with open(file, encoding="utf-8") as data_file:
                match = re_.match(data_file.readline())
                if match:
                    schema = match.group(1)

        data: Dict[str, Any] = {}
        if is_yaml:
            with open(file, encoding="utf-8") as data_file:
                data = yaml.load(data_file)
        elif is_json:
            with open(file, encoding="utf-8") as data_file:
                data = json.load(data_file)

        if args.schema is None:
            schema = data.get("$schema")

        if schema is None:
            print(f"Could not find the schema for {file}")
            sys.exit(1)

        if schema.startswith("http://"):
            if urlparse.urlparse(schema).scheme != "":
                with open(schema, encoding="utf-8") as schema_file:
                    schema_data = json.load(schema_file)
            else:
                response = requests.get(schema, timeout=args.timeout)
                if not response.ok:
                    print(f"Could not load the schema {schema}")
                    sys.exit(1)

                schema_data = response.json()
        validate(file, data, schema_data)
