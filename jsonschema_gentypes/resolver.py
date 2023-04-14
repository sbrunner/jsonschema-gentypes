"""
Resolve references in a JSON schema.

Encapsulate the referencing logic to be able to use it in the code generation.
"""

import json
import re
from typing import Any, Dict, List, Optional, Union, cast

import requests
from referencing import Registry, Resource

from jsonschema_gentypes import (
    jsonschema_draft_04,
    jsonschema_draft_2019_09_core,
    jsonschema_draft_2020_12_applicator,
    jsonschema_draft_2020_12_core,
)

Json = Union[str, int, float, bool, None, List["Json"], Dict[str, "Json"]]
JsonDict = Dict[str, "Json"]

_RESOURCE_CACHE: Dict[str, Resource[Any]] = {}


def _open_uri(uri: str) -> Json:
    if uri.startswith("http://") or uri.startswith("https://"):
        response = requests.get(uri, timeout=30)
        return cast(Json, response.json())
    else:
        with open(uri, encoding="utf-8") as open_file:
            return cast(Json, json.load(open_file))


def _open_uri_resolver(uri: str) -> Resource[Any]:
    if uri in _RESOURCE_CACHE:
        return _RESOURCE_CACHE[uri]
    my_resource = Resource.from_contents(_open_uri(uri))
    _RESOURCE_CACHE[uri] = my_resource
    return my_resource


_URL_PREFIX = "https://json-schema.org/draft/"
_VOCAB_URL_RE = re.compile(rf"{re.escape(_URL_PREFIX)}([0-9-]+)/vocab/(.+)$")
_META_RE = re.compile(r"^meta/([a-zA-Z0-9]+)#(.*)$")


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
                jsonschema_draft_2019_09_core.JSONSchemaItemD2019,
                jsonschema_draft_2020_12_core.JSONSchemaItemD2020,
            ]
        ] = None,
    ) -> None:
        """Initialize the resolver."""
        self.base_url = base_url
        self.schema = (
            cast(
                Union[
                    jsonschema_draft_2019_09_core.JSONSchemaItemD2019,
                    jsonschema_draft_2020_12_core.JSONSchemaItemD2020,
                ],
                _open_uri(base_url),
            )
            if schema is None
            else schema
        )
        if "$schema" in self.schema:
            _RESOURCE_CACHE[base_url] = Resource.from_contents(self.schema)

        registry = Registry(retrieve=_open_uri_resolver)  # type: ignore
        self.resolver = registry.resolver()

        self.vocabulary: Dict[str, str] = {}
        for vocab, value in self.schema.get("$vocabulary", {}).items():
            if value is True:
                vocab_match = _VOCAB_URL_RE.match(vocab)
                if vocab_match:
                    version, vocab = vocab_match.groups()
                    self.add_vocabulary(vocab, f"{_URL_PREFIX}{version}/meta/{vocab}")

    def add_vocabulary(self, vocab: str, url: str) -> None:
        """Add a vocabulary to the resolver."""
        self.vocabulary[vocab] = url

    def lookup(
        self, uri: str
    ) -> Union[jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020]:
        """Lookup for the reference."""
        match = _META_RE.match(uri)
        if match:
            vocab, path = match.groups()
            if vocab in self.vocabulary:
                return cast(
                    Union[
                        jsonschema_draft_04.JSONSchemaD4,
                        jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020,
                    ],
                    self.resolver.lookup(f"{self.vocabulary[vocab]}#{path}").contents,
                )
        if uri.startswith("#"):
            return cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                self.resolver.lookup(f"{self.base_url}{uri}").contents,
            )
        else:
            return cast(
                Union[
                    jsonschema_draft_04.JSONSchemaD4, jsonschema_draft_2020_12_applicator.JSONSchemaItemD2020
                ],
                self.resolver.lookup(uri).contents,
            )
