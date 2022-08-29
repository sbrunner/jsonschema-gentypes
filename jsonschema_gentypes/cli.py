"""
Generate the Python type files from the JSON schema files.
"""

import argparse
import json
import logging
import os
import pkgutil
import random
import re
import subprocess  # nosec
import sys
from typing import Dict, Set, cast

import requests
import ruamel.yaml
from jsonschema import RefResolver

import jsonschema_gentypes
from jsonschema_gentypes import configuration, validate

LOG = logging.getLogger(__name__)


def _add_type(
    type_: jsonschema_gentypes.Type,
    imports: Dict[str, Set[str]],
    types: Dict[str, jsonschema_gentypes.Type],
    gen: configuration.GenerateItem,
    config: configuration.Configuration,
) -> None:
    if (
        isinstance(type_, jsonschema_gentypes.NamedType)
        and type_.unescape_name() in types
        and type_.definition(config.get("lineLength"))
        == types[type_.unescape_name()].definition(config.get("lineLength"))
    ):
        return
    name_mapping = gen.get("name_mapping", {})
    assert name_mapping is not None
    if isinstance(type_, jsonschema_gentypes.NamedType) and type_.unescape_name() in name_mapping:
        type_.set_name(name_mapping[type_.unescape_name()])
    if isinstance(type_, jsonschema_gentypes.NamedType) and type_.unescape_name() in types:
        print(f"WARNING: the type {type_.unescape_name()} is already defined, it will be renamed")
        type_.postfix_name(f"Gen{random.randrange(999999)}")  # nosec
        _add_type(type_, imports, types, gen, config)
    else:
        if isinstance(type_, jsonschema_gentypes.NamedType):
            types[type_.unescape_name()] = type_
        for package, imp in type_.imports():
            if package not in imports:
                imports[package] = set()
            imports[package].add(imp)
        for sub_type in type_.depends_on():
            _add_type(sub_type, imports, types, gen, config)


def main() -> None:
    """
    Generate the Python type files from the JSON schema files.
    """
    parser = argparse.ArgumentParser(usage="Generate the Python type files from the JSON schema files")
    parser.add_argument("--config", default="jsonschema-gentypes.yaml", help="The configuration file")
    parser.add_argument("--skip-config-errors", action="store_true", help="Skip the configuration error")
    parser.add_argument("--json-schema", help="The JSON schema")
    parser.add_argument("--python", help="The generated python file")
    args = parser.parse_args()

    if args.python is not None or args.json_schema is not None:
        if args.python is None or args.json_schema is None:
            print("If you specify the argument --python or --json-schema the other one is required")
            sys.exit(1)
        config: configuration.Configuration = {
            "generate": [{"source": args.json_schema, "destination": args.python}]
        }
    else:
        schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")
        assert schema_data
        with open(args.config, encoding="utf-8") as data_file:
            yaml = ruamel.yaml.YAML()
            data = yaml.load(data_file)
        errors, data = validate.validate(args.config, data, json.loads(schema_data), True)
        config = cast(configuration.Configuration, data)

        if errors:
            LOG.error("The config file is invalid:\n%s", "\n".join(errors))
            if not args.skip_config_errors:
                sys.exit(1)

    for gen in config["generate"]:
        source = gen["source"]
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source, timeout=60)
            response.raise_for_status()
            schema = response.json()
        else:
            with open(os.path.abspath(source), encoding="utf-8") as source_file:
                schema = json.load(source_file)

        resolver: RefResolver = RefResolver.from_schema(schema)
        schema_ref = schema.get("$schema", "default")
        schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
        api_version = {
            "draft-04": jsonschema_gentypes.APIv4,
            "draft-06": jsonschema_gentypes.APIv6,
            "draft-07": jsonschema_gentypes.APIv7,
        }.get(
            schema_match.group(1) if schema_match else "default",
            jsonschema_gentypes.APIv7,
        )
        api_args = gen.get("api_arguments", {})
        api = api_version(resolver, **api_args)

        types: Dict[str, jsonschema_gentypes.Type] = {}
        imports: Dict[str, Set[str]] = {}

        base_type = api.get_type(schema, gen.get("root_name", "Root"))
        if "root_name" in gen and isinstance(base_type, jsonschema_gentypes.NamedType):
            assert gen["root_name"] is not None
            base_type.set_name(gen["root_name"])
        _add_type(base_type, imports, types, gen, config)

        lines = []
        for imp, names in imports.items():
            lines.append(f'from {imp} import {", ".join(names)}')

        for type_ in sorted(types.values(), key=lambda type_: type_.name()):
            lines += type_.definition(config.get("lineLength"))

        with open(gen["destination"], "w", encoding="utf-8") as destination_file:
            headers = config.get("headers")
            if headers:
                destination_file.write(headers)
                destination_file.write("\n\n")
            destination_file.write("\n".join(lines))
            destination_file.write("\n")

        callbacks = config.get("callbacks", [])
        assert callbacks is not None
        for callback in callbacks:
            cmd = list(callback)
            cmd.append(gen["destination"])
            subprocess.check_call(cmd)  # nosec
