import json
import logging
import pkgutil
import re
import sys
from typing import Any, Dict, Iterator, List, TextIO, Tuple, Union

import jsonschema
import ruamel.yaml

import jsonschema_gentypes.jsonschema

LOG = logging.getLogger(__name__)


def _extend_with_default(
    validator_class: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
) -> "jsonschema.validators._DefaultTypesDeprecatingMetaClass":
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(
        validator: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
        properties: Dict[str, jsonschema_gentypes.jsonschema.JSONSchemaItem],
        instance: Any,
        schema: jsonschema_gentypes.jsonschema.JSONSchemaItem,
    ) -> Iterator[jsonschema.exceptions.ValidationError]:
        for prop, subschema in properties.items():
            if "$ref" in subschema:
                ref = subschema["$ref"]
                resolve = getattr(validator.resolver, "resolve", None)
                if resolve is None:
                    with validator.resolver.resolving(ref) as resolved:
                        for error in validator.descend(instance, resolved):
                            yield error
                else:
                    _, resolved = validator.resolver.resolve(ref)
                    subschema = dict(subschema)  # type: ignore
                    subschema.update(resolved)
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def validate_error(
    filename: str, data_file: Union[TextIO, str], schema: Dict[str, Any], default: bool = True
) -> Tuple[List[str], Dict[str, Any]]:
    data = ruamel.yaml.round_trip_load(data_file)  # type: ignore

    schema_ref = schema.get("$schema", "default")
    schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
    Validator = {  # noqa: N806 # variable 'Validator' in function should be lowercase
        "draft-04": jsonschema.Draft4Validator,
        "draft-06": jsonschema.Draft6Validator,
        "draft-07": jsonschema.Draft7Validator,
    }.get(
        schema_match.group(1) if schema_match else "default",
        jsonschema.Draft7Validator,
    )
    if default:
        Validator = _extend_with_default(  # noqa: N806 # variable 'Validator' in function should be lowercase
            Validator
        )

    validator = Validator(schema)

    def format_error(error: jsonschema.exceptions.ValidationError) -> str:
        position = filename

        if hasattr(error.instance, "lc"):
            position = f"{filename}:{error.instance.lc.line + 1}:{error.instance.lc.col + 1}"
        else:
            curent_data = data
            parent = None
            if hasattr(curent_data, "lc"):
                parent = curent_data
            for path in error.path:
                curent_data = curent_data[path]
                if hasattr(curent_data, "lc"):
                    parent = curent_data
            if parent is not None:
                position = f"{filename}:{parent.lc.line + 1}:{parent.lc.col + 1}"

        return (
            f" - {position} "
            f'({".".join([str(i) for i in error.path] if error.path else "/")}): '
            f"{error.message} (rule: "
            f'{".".join([str(i) for i in error.schema_path] if error.schema_path else "/")})'
        )

    return sorted([format_error(e) for e in validator.iter_errors(data)]), data


def validate(
    filename: str,
    schema_data: Union[bytes, str],
    default: bool = True,
    use_logger: bool = True,
    exit_on_error: bool = True,
) -> Any:
    with open(filename) as data_file:
        errors, data = validate_error(filename, data_file, json.loads(schema_data), default)

    if errors:
        if use_logger:
            LOG.error("The config file is invalid:\n%s", "\n".join(errors))
        else:
            print("The config file is invalid.\n{}".format("\n".join(errors)))
        if exit_on_error:
            sys.exit(1)

    return data


def validate_package(filename: str, schema_package: str, schema_filename: str, **kwargs: Any) -> Any:
    schema_data = pkgutil.get_data(schema_package, schema_filename)
    assert schema_data
    return validate(filename, schema_data, **kwargs)
