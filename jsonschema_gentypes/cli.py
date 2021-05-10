import argparse
import json
import os
import pkgutil
import random
import re
import subprocess
import sys
from typing import Dict, Set

import jsonschema
import requests
import yaml
from jsonschema import RefResolver

import jsonschema_gentypes
from jsonschema_gentypes import configuration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="jsonschema-gentypes.yaml", help="The configuration file")
    parser.add_argument("--skip-config-errors", action="store_true", help="Skip the configuration error")
    args = parser.parse_args()

    with open(args.config) as config_file:
        config: configuration.Configuration = yaml.load(config_file, Loader=yaml.SafeLoader)

    schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")
    assert schema_data is not None
    validator = jsonschema.Draft7Validator(schema=json.loads(schema_data))
    errors = sorted(
        [
            f' - {".".join([str(i) for i in e.path] if e.path else "/")}: {e.message}'
            for e in validator.iter_errors(config)
        ]
    )
    if errors:
        print("The config file is invalid.\n{}".format("\n".join(errors)))
        if not args.skip_config_errors:
            sys.exit(1)

    for gen in config["generate"]:
        source = gen["source"]
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source)
            response.raise_for_status()
            schema = response.json()
        else:
            with open(os.path.abspath(source)) as source_file:
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
        imports: Dict[str, Set[str]] = dict()

        def add_type(
            type_: jsonschema_gentypes.Type,
            imports: Dict[str, Set[str]],
            types: Dict[str, jsonschema_gentypes.Type],
            gen: configuration.GenerateItem,
        ) -> None:
            if (
                isinstance(type_, jsonschema_gentypes.NamedType)
                and type_.unescape_name() in types
                and type_.definition() == types[type_.unescape_name()].definition()
            ):
                return
            name_mapping = gen.get("name_mapping", {})
            assert name_mapping is not None
            if isinstance(type_, jsonschema_gentypes.NamedType) and type_.unescape_name() in name_mapping:
                type_.set_name(name_mapping[type_.unescape_name()])
            if isinstance(type_, jsonschema_gentypes.NamedType) and type_.unescape_name() in types:
                print(f"WARNING: the type {type_.unescape_name()} is already defined, it will be renamed")
                type_.postfix_name(f"Gen{random.randrange(999999)}")
                add_type(type_, imports, types, gen)
            else:
                if isinstance(type_, jsonschema_gentypes.NamedType):
                    types[type_.unescape_name()] = type_
                for package, imp in type_.imports():
                    if package not in imports:
                        imports[package] = set()
                    imports[package].add(imp)
                for sub_type in type_.depends_on():
                    add_type(sub_type, imports, types, gen)

        base_type = api.get_type(schema, gen.get("root_name", "Root"))
        if "root_name" in gen and isinstance(base_type, jsonschema_gentypes.NamedType):
            assert gen["root_name"] is not None
            base_type.set_name(gen["root_name"])
        add_type(base_type, imports, types, gen)

        lines = []
        for imp, names in imports.items():
            lines.append(f'from {imp} import {", ".join(names)}')

        for type_ in sorted(types.values(), key=lambda type_: type_.name()):
            lines += type_.definition()

        with open(gen["destination"], "w") as destination_file:
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
            subprocess.check_call(cmd)
