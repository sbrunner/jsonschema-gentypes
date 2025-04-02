"""
Resolve references in a JSON schema.

Encapsulate the referencing logic to be able to use it in the code generation.
"""

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union, cast

import referencing._core
import referencing.exceptions
import requests
import yaml

from jsonschema_gentypes import (
    jsonschema_draft_04,
    jsonschema_draft_06,
    jsonschema_draft_2020_12_applicator,
)

if TYPE_CHECKING:
    from jsonschema_gentypes import (
        jsonschema_draft_2019_09_core,
        jsonschema_draft_2020_12_core,
    )

Json = Union[str, int, float, bool, None, list["Json"], dict[str, "Json"]]
JsonDict = dict[str, "Json"]

_RESOURCE_CACHE: dict[str, referencing.Resource[Any]] = {}


def _openapi_schema(
    config: Union[
        jsonschema_draft_06.JSONSchemaItemD6,
        jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
    ],
) -> Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
    if "$schema" not in config and "openapi" in config:
        config_core = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            config,
        )
        config_core["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return config


def _open_uri(
    uri: str,
) -> Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
    if uri.startswith(("http://", "https://")):
        response = requests.get(uri, timeout=30)
        return _openapi_schema(
            cast(
                "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                response.json(),
            ),
        )
    with Path(uri).open(encoding="utf-8") as open_file:
        file_content = open_file.read()
        try:
            schema = yaml.load(file_content, Loader=yaml.SafeLoader)
        except Exception:  # pylint: disable=broad-except # noqa: BLE001
            schema = json.loads(file_content)
        return _openapi_schema(
            cast(
                "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                schema,
            ),
        )


def _open_uri_resolver(uri: str) -> referencing.Resource[Any]:
    if uri in _RESOURCE_CACHE:
        return _RESOURCE_CACHE[uri]
    my_resource = referencing.Resource.from_contents(_open_uri(uri))
    _RESOURCE_CACHE[uri] = my_resource
    return my_resource


_URL_PREFIX = "https://json-schema.org/draft/"
_VOCAB_URL_RE = re.compile(rf"{re.escape(_URL_PREFIX)}([0-9-]+)/vocab/(.+)$")
_META_RE = re.compile(r"^meta/([a-zA-Z0-9]+)#(.*)$")


class UnRedolvedError(Exception):
    """Exception for unresolved references."""


class RefResolver:
    """
    Resolve references in a JSON schema.

    Encapsulate the referencing logic to be able to use it in the code generation.
    """

    def __init__(
        self,
        base_url: str,
        schema: Optional[
            Union[
                jsonschema_draft_06.JSONSchemaItemD6,
                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
            ]
        ] = None,
    ) -> None:
        """
        Initialize the resolver.

        Parameter:
            base_url: The base URL of the schema.
            schema: The schema to resolve.
        """
        schema = _openapi_schema(schema) if schema is not None else None
        self.schema = _open_uri(base_url) if schema is None else schema
        schema_vocabulary = cast(
            "Union[jsonschema_draft_2019_09_core.JSONSchemaItemD2019, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            self.schema,
        )
        if "$schema" in self.schema:
            _RESOURCE_CACHE[base_url] = referencing.Resource.from_contents(self.schema)

        self.registry = referencing.Registry(retrieve=_open_uri_resolver)  # type: ignore[call-arg]
        self.resolver: referencing._core.Resolver[
            Union[
                jsonschema_draft_06.JSONSchemaItemD6,
                jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
            ]
        ] = self.registry.resolver(base_url)

        self.vocabulary_url: dict[str, str] = {}
        self.vocabulary_resolver: dict[
            str,
            referencing._core.Resolver[
                Union[
                    jsonschema_draft_06.JSONSchemaItemD6,
                    jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                ]
            ],
        ] = {}

        for vocab, value in schema_vocabulary.get("$vocabulary", {}).items():
            if value is True:
                vocab_match = _VOCAB_URL_RE.match(vocab)
                if vocab_match:
                    version, sub_vocab = vocab_match.groups()
                    self.add_vocabulary(sub_vocab, f"{_URL_PREFIX}{version}/meta/{sub_vocab}")

    def add_vocabulary(self, vocab: str, url: str) -> None:
        """Add a vocabulary to the resolver."""
        self.vocabulary_url[vocab] = url
        self.vocabulary_resolver[vocab] = self.registry.resolver(url)

    def add_local_resource(self, content_path: Union[str, Path]) -> None:
        """Add some locally available resource to the registry."""
        with Path(content_path).open("r", encoding="utf-8") as f:
            content = json.load(f)
        self.registry = self.registry.with_contents([(content["$id"], content)])

    def lookup(
        self,
        uri: str,
    ) -> Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """
        Lookup for the reference.

        Parameter:
            uri: The reference to lookup.
        """
        match = _META_RE.match(uri)
        if match:
            vocab, path = match.groups()
            if vocab in self.vocabulary_url.values():
                return self.resolver.lookup(f"{self.vocabulary_url[vocab]}#{path}").contents

        exception = None
        if uri in self.registry:
            return cast(
                "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
                self.registry[uri].contents,
            )
        try:
            return self.resolver.lookup(uri).contents
        except (
            referencing.exceptions.NoSuchResource,
            referencing.exceptions.PointerToNowhere,
        ) as curent_exeption:
            exception = curent_exeption
            for resolver in self.vocabulary_resolver.values():
                try:
                    return resolver.lookup(uri).contents
                except (referencing.exceptions.NoSuchResource, referencing.exceptions.PointerToNowhere):
                    pass
        message = f"Ref '{uri}' not found"
        raise UnRedolvedError(message) from exception

    def auto_resolve(
        self,
        config: Union[
            jsonschema_draft_04.JSONSchemaD4,
            jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
        ],
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """
        Resolve if the config has a $ref key.

        Parameter:
            config: The config to resolve.
        """
        config_with_ref = cast(
            "Union[jsonschema_draft_06.JSONSchemaItemD6, jsonschema_draft_2020_12_core.JSONSchemaItemD2020]",
            config,
        )
        return cast(
            "Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]",
            self.lookup(config_with_ref["$ref"]) if "$ref" in config_with_ref else config,
        )
