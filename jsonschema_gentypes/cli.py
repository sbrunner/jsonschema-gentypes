"""
Generate the Python type files from the JSON schema files.
"""

import argparse
import logging
import os
import pkgutil
import random
import re
import subprocess  # nosec
import sys
from typing import Dict, Optional, Set, Tuple, cast

import yaml

import jsonschema_gentypes.api
import jsonschema_gentypes.api_draft_04
import jsonschema_gentypes.api_draft_06
import jsonschema_gentypes.api_draft_07
import jsonschema_gentypes.api_draft_2019_09
import jsonschema_gentypes.api_draft_2020_12
import jsonschema_gentypes.resolver
from jsonschema_gentypes import configuration

LOG = logging.getLogger(__name__)


def _add_type(
    type_: jsonschema_gentypes.Type,
    imports: Dict[str, Set[str]],
    types: Dict[str, jsonschema_gentypes.Type],
    gen: configuration.GenerateItem,
    config: configuration.Configuration,
    minimal_python_version: Tuple[int, ...],
    added_types: Optional[Set[jsonschema_gentypes.Type]] = None,
) -> None:
    if added_types is None:
        added_types = set()
    if type_ in added_types:
        return
    added_types.add(type_)
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
        _add_type(type_, imports, types, gen, config, minimal_python_version, added_types)
    else:
        if isinstance(type_, jsonschema_gentypes.NamedType):
            types[type_.unescape_name()] = type_
        for package, imp in type_.imports(minimal_python_version):
            if package not in imports:
                imports[package] = set()
            imports[package].add(imp)
        for sub_type in type_.depends_on():
            _add_type(sub_type, imports, types, gen, config, minimal_python_version, added_types)


def main() -> None:
    """
    Generate the Python type files from the JSON schema files.
    """
    parser = argparse.ArgumentParser(usage="Generate the Python type files from the JSON schema files")
    parser.add_argument("--config", default="jsonschema-gentypes.yaml", help="The configuration file")
    parser.add_argument("--skip-config-errors", action="store_true", help="Skip the configuration error")
    parser.add_argument("--json-schema", help="The JSON schema")
    parser.add_argument("--python", help="The generated Python file")
    parser.add_argument(
        "--python-version", help="The minimal Python version that will support the generate type stubs."
    )
    args = parser.parse_args()

    if args.python is not None or args.json_schema is not None:
        if args.python is None or args.json_schema is None:
            print("If you specify the argument --python or --json-schema the other one is required")
            sys.exit(1)

        config: configuration.Configuration = {
            "python_version": args.python_version,
            "generate": [
                {
                    "source": args.json_schema,
                    "destination": args.python,
                }
            ],
        }
    else:
        schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")
        assert schema_data
        with open(args.config, encoding="utf-8") as data_file:
            data = yaml.load(data_file, Loader=yaml.SafeLoader)
        config = cast(configuration.Configuration, data)

    process_config(config)


def process_config(config: configuration.Configuration) -> None:
    """
    Run the tasks defined in the given configuration.
    """

    str_python_version = config.get("python_version")
    if str_python_version is not None:
        python_version = tuple(int(x) for x in str_python_version.split("."))
    else:
        python_version = sys.version_info[:3]

    for gen in config["generate"]:
        source = gen["source"]
        print(f"Processing {source}")

        resolver = jsonschema_gentypes.resolver.RefResolver(source)
        schema = resolver.schema

        if "vocabularies" in gen:
            for vocab, uri in gen["vocabularies"].items():
                resolver.add_vocabulary(vocab, uri)

        schema_ref = schema.get("$schema", "default")
        schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
        api_version = {
            "draft-04": jsonschema_gentypes.api_draft_04.APIv4,
            "draft-06": jsonschema_gentypes.api_draft_06.APIv6,
            "draft-07": jsonschema_gentypes.api_draft_07.APIv7,
            "draft/2019-09": jsonschema_gentypes.api_draft_2019_09.APIv201909,
            "draft/2020-12": jsonschema_gentypes.api_draft_2020_12.APIv202012,
        }.get(
            schema_match.group(1) if schema_match else "default",
            jsonschema_gentypes.api_draft_2019_09.APIv201909,
        )
        api_args = gen.get("api_arguments", {})
        api = api_version(resolver, **api_args)

        types: Dict[str, jsonschema_gentypes.Type] = {}
        imports: Dict[str, Set[str]] = {}

        root_name = gen.get("root_name", "Root")
        base_type = api.get_type(schema, root_name)
        if "root_name" in gen and isinstance(base_type, jsonschema_gentypes.NamedType):
            assert gen["root_name"] is not None
            base_type.set_name(gen["root_name"])

        _add_type(base_type, imports, types, gen, config, python_version)

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

        pre_commit = config.get("pre_commit", {})
        if pre_commit.get("enabled", False):
            env = {**os.environ}
            env["SKIP"] = ",".join(pre_commit.get("hooks_skip", []))
            subprocess.run(  # nosec
                [
                    "pre-commit",
                    "run",
                    *pre_commit.get("arguments", []),
                    f"--files={gen['destination']}",
                    *pre_commit.get("hooks", []),
                ],  # nosec
                env=env,
                check=False,
            )

        callbacks = config.get("callbacks", [])
        assert callbacks is not None
        for callback in callbacks:
            cmd = list(callback)
            cmd.append(gen["destination"])
            subprocess.run(cmd, check=True)  # nosec
