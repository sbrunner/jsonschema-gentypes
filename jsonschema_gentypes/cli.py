"""Generate the Python type files from the JSON schema files."""

import argparse
import json
import logging
import os
import pkgutil
import random
import re
import subprocess  # nosec
import sys
from pathlib import Path
from typing import Any, Callable, Optional, Union, cast

import yaml

import jsonschema_gentypes.api
import jsonschema_gentypes.api_draft_04
import jsonschema_gentypes.api_draft_06
import jsonschema_gentypes.api_draft_07
import jsonschema_gentypes.api_draft_2019_09
import jsonschema_gentypes.api_draft_2020_12
import jsonschema_gentypes.resolver
from jsonschema_gentypes import (
    configuration,
    jsonschema_draft_04,
    jsonschema_draft_2020_12_applicator,
)

LOG = logging.getLogger(__name__)


def _add_type(
    type_: jsonschema_gentypes.Type,
    imports: dict[str, set[str]],
    types: dict[str, jsonschema_gentypes.Type],
    gen: configuration.GenerateItem,
    config: configuration.Configuration,
    python_version: tuple[int, ...],
    added_types: Optional[set[jsonschema_gentypes.Type]] = None,
) -> None:
    if added_types is None:
        added_types = set()

    if type_ in added_types:
        return
    added_types.add(type_)
    if (
        isinstance(type_, jsonschema_gentypes.NamedType)
        and type_.name(python_version) in types
        and type_.definition(python_version, config.get("lineLength"))
        == types[type_.name(python_version)].definition(python_version, config.get("lineLength"))
    ):
        return
    name_mapping = gen.get("name_mapping", {})
    assert name_mapping is not None
    if isinstance(type_, jsonschema_gentypes.NamedType) and type_.unescape_name() in name_mapping:
        type_.set_name(name_mapping[type_.unescape_name()])
    if isinstance(type_, jsonschema_gentypes.NamedType) and type_.name(python_version) in types:
        if types[type_.name(python_version)] != type_:
            print(f"WARNING: the type {type_.name(python_version)} is already defined, it will be renamed")
            type_.postfix_name(f"Gen{random.randrange(999999)}")  # noqa: S311 # nosec
            _add_type(type_, imports, types, gen, config, python_version, added_types)
    else:
        if isinstance(type_, jsonschema_gentypes.NamedType):
            types[type_.name(python_version)] = type_
        for package, imp in type_.imports(python_version):
            if package not in imports:
                imports[package] = set()
            imports[package].add(imp)
        for sub_type in type_.depends_on(python_version):
            _add_type(sub_type, imports, types, gen, config, python_version, added_types)


def main() -> None:
    """Generate the Python type files from the JSON schema files."""
    parser = argparse.ArgumentParser(usage="Generate the Python type files from the JSON schema files")
    parser.add_argument(
        "--config",
        type=Path,
        default="jsonschema-gentypes.yaml",
        help="The configuration file",
    )
    parser.add_argument(
        "--skip-config-validation",
        action="store_false",
        dest="config_validation",
        help="Skip the configuration error",
    )
    parser.add_argument("--json-schema", help="The JSON schema")
    parser.add_argument("--python", help="The generated Python file")
    parser.add_argument(
        "--python-version",
        help="The minimal Python version that will support the generate type stubs.",
    )
    parser.add_argument("files", nargs="*", help="The JSON schema files")
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
                },
            ],
        }
    else:
        data: Any = None
        if args.config_validation:
            data = validate_config(args.config)
        if data is None:
            with args.config.open(encoding="utf-8") as data_file:
                data = yaml.load(data_file, Loader=yaml.SafeLoader)
        config = cast("configuration.Configuration", data)

    process_config(config, args.files)


def validate_config(config_path: Path) -> Optional[Any]:
    """Validate the configuration file."""

    try:
        import jsonschema_validator  # pylint: disable=import-outside-toplevel
        import ruamel.yaml  # pylint: disable=import-outside-toplevel
    except ImportError:
        print("Please install the dependencies to validate the configuration file")
        print("pip install jsonschema-gentypes[validation]")
        return None

    schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")
    assert schema_data
    schema = json.loads(schema_data)

    with config_path.open(encoding="utf-8") as data_file:
        ru_yaml = ruamel.yaml.YAML()
        data = ru_yaml.load(data_file)

    errors, _ = jsonschema_validator.validate(str(config_path), data, schema)
    if errors:
        print("\n".join(errors))
        sys.exit(1)

    return data


class _AddType:
    def __init__(
        self,
        api: jsonschema_gentypes.api.API,
        resolver: jsonschema_gentypes.resolver.RefResolver,
        imports: dict[str, set[str]],
        types: dict[str, jsonschema_gentypes.Type],
        gen: configuration.GenerateItem,
        config: configuration.Configuration,
        python_version: tuple[int, ...],
    ) -> None:
        self.api = api
        self.resolver = resolver
        self.imports = imports
        self.types = types
        self.gen = gen
        self.config = config
        self.python_version = python_version

    def __call__(
        self,
        schema: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
        name: str,
        force_name: bool = True,
    ) -> jsonschema_gentypes.Type:
        base_type = self.api.get_type(self.resolver.auto_resolve(schema), name)
        if force_name and isinstance(base_type, jsonschema_gentypes.NamedType):
            base_type.set_name(name)

        _add_type(base_type, self.imports, self.types, self.gen, self.config, self.python_version)
        return base_type


class _BuildName:
    def __init__(self, gen: configuration.GenerateItem) -> None:
        self.gen = gen

    def __call__(self, path: str, parts: list[str]) -> str:
        parts = [*path.split("/"), *parts]
        self.gen.get("root_name")
        if "root_name" in self.gen:
            parts = [self.gen["root_name"], *parts]
        parts = [x.replace("{", "").replace("}", "") for x in parts]
        parts = [x.lower() for x in parts if x]
        parts = [x[0].upper() + x[1:] for x in parts]
        return "".join(parts)


def process_config(config: configuration.Configuration, files: list[str]) -> None:
    """
    Run the tasks defined in the given configuration.

    Parameter:
        config: The configuration.
        files: The files to process.
    """
    str_python_version = config.get("python_version")
    if str_python_version is not None:
        python_version = tuple(int(x) for x in str_python_version.split("."))
    else:
        python_version = sys.version_info[:3]

    for gen in config["generate"]:
        if jsonschema_gentypes.get_name.__dict__.get("names"):
            del jsonschema_gentypes.get_name.__dict__["names"]
        source = gen["source"]
        if files and source not in files:
            continue
        print(f"Processing {source}")

        resolver = jsonschema_gentypes.resolver.RefResolver(source)
        schema = resolver.schema

        if "vocabularies" in gen:
            for vocab, uri in gen["vocabularies"].items():
                resolver.add_vocabulary(vocab, uri)

        if "local_resources" in gen:
            for path in gen["local_resources"]:
                resolver.add_local_resource(path)

        openapi = "openapi" in schema
        if "$schema" not in schema and openapi:
            api_version: Callable[..., Any] = jsonschema_gentypes.api_draft_2020_12.APIv202012
        else:
            schema_ref = schema.get("$schema", "default")
            assert isinstance(schema_ref, str)
            schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
            api_version = {
                "draft-04": jsonschema_gentypes.api_draft_04.APIv4,
                "draft-06": jsonschema_gentypes.api_draft_06.APIv6,
                "draft-07": jsonschema_gentypes.api_draft_07.APIv7,
                "draft/2019-09": jsonschema_gentypes.api_draft_2019_09.APIv201909,
                "draft/2020-12": jsonschema_gentypes.api_draft_2020_12.APIv202012,
            }.get(
                schema_match.group(1) if schema_match else "default",
                jsonschema_gentypes.api_draft_2020_12.APIv202012,
            )
        api_args = gen.get("api_arguments", {})
        api = api_version(resolver, python_version=python_version, **api_args)

        types: dict[str, jsonschema_gentypes.Type] = {}
        imports: dict[str, set[str]] = {}

        add_type = _AddType(api, resolver, imports, types, gen, config, python_version)

        if openapi:
            build_name = _BuildName(gen)

            for path_name, path_config in schema.get("paths", {}).items():  # type: ignore[attr-defined]
                path_config = resolver.auto_resolve(path_config)  # noqa: PLW2901
                for method_name, method_config in path_config.items():
                    method_config = resolver.auto_resolve(method_config)  # noqa: PLW2901

                    global_type: dict[str, jsonschema_gentypes.Type] = {}
                    global_type_required = set()

                    # Add request parameters
                    classed_parameters: dict[str, dict[str, jsonschema_gentypes.Type]] = {}
                    classed_parameters_required: dict[str, set[str]] = {}
                    for param_config in method_config.get("parameters", []):
                        param_config = resolver.auto_resolve(param_config)  # noqa: PLW2901
                        classed_parameters.setdefault(param_config["in"], {})[param_config["name"]] = (
                            add_type(
                                param_config["schema"],
                                build_name(
                                    path_name,
                                    [method_name, param_config["in"], param_config["name"]],
                                ),
                            )
                        )
                        if param_config.get("required", param_config["in"] == "path"):
                            classed_parameters_required.setdefault(param_config["in"], set()).add(
                                param_config["name"],
                            )

                    for param_in, param_configs in classed_parameters.items():
                        global_type_required.add(param_in)
                        description = f"Parameter type '{param_in}' of request on path '{path_name}', using method '{method_name}'."
                        type_: jsonschema_gentypes.Type = jsonschema_gentypes.TypedDictType(
                            build_name(
                                path_name,
                                [method_name, param_in],
                            ),
                            param_configs,
                            (
                                [description, "", "Request summary:", method_config["summary"]]
                                if "summary" in method_config
                                else [description]
                            ),
                            classed_parameters_required.get(param_in, set()),
                        )
                        global_type[param_in] = type_
                        _add_type(type_, imports, types, gen, config, python_version)

                    # Add request body
                    if "requestBody" in method_config:
                        method_config = resolver.auto_resolve(method_config)  # noqa: PLW2901
                        for content_type, content_config in (
                            method_config.get("requestBody", {}).get("content", {}).items()
                        ):
                            content_config = resolver.auto_resolve(content_config)  # noqa: PLW2901
                            if content_type == "application/json" and "schema" in content_config:
                                global_type_required.add("request_body")
                                global_type["request_body"] = add_type(
                                    content_config["schema"],
                                    build_name(path_name, [method_name, "requestBody"]),
                                )

                    # Add responses
                    all_responses = []
                    for response_code, response_config in method_config.get("responses", {}).items():
                        response_config = resolver.auto_resolve(response_config)  # noqa: PLW2901
                        for content_type, content_config in response_config.get("content", {}).items():
                            content_config = resolver.auto_resolve(content_config)  # noqa: PLW2901
                            if content_type == "application/json" and "schema" in content_config:
                                all_responses.append(
                                    add_type(
                                        content_config["schema"],
                                        build_name(
                                            path_name,
                                            [method_name, "response", str(response_code)],
                                        ),
                                    ),
                                )
                    type_ = jsonschema_gentypes.TypeAlias(
                        build_name(
                            path_name,
                            [method_name, "response"],
                        ),
                        jsonschema_gentypes.UnionType(all_responses),
                    )
                    global_type["response"] = type_
                    _add_type(type_, imports, types, gen, config, python_version)

                    description = (
                        f"Description of request on path '{path_name}', using method '{method_name}'."
                    )
                    _add_type(
                        jsonschema_gentypes.TypedDictType(
                            build_name(
                                path_name,
                                [method_name],
                            ),
                            global_type,
                            (
                                [description, "", method_config["summary"]]
                                if "summary" in method_config
                                else [description]
                            ),
                            global_type_required,
                        ),
                        imports,
                        types,
                        gen,
                        config,
                        python_version,
                    )
        else:
            schema_all = cast(
                "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                schema,
            )
            add_type(schema_all, gen.get("root_name", "Root"), force_name="root_name" in gen)

        lines = []
        for imp, names in imports.items():
            lines.append(f"from {imp} import {', '.join(sorted(names))}")

        for type_2 in sorted(types.values(), key=lambda type_3: type_3.name(python_version)):
            lines += type_2.definition(python_version, config.get("lineLength"))

        with Path(gen["destination"]).open("w", encoding="utf-8") as destination_file:
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
            subprocess.run(  # noqa: S603
                [  # noqa: S607
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
            subprocess.run(cmd, check=True)  # noqa: S603
