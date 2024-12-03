"""Automatically generated file from a JSON schema."""

from typing import TypedDict, Union

ContentVocabularyMetaSchema = Union["_ContentVocabularyMetaSchemaObject", bool]
""" Content vocabulary meta-schema. """


class _ContentVocabularyMetaSchemaObject(TypedDict, total=False):
    contentMediaType: str
    contentEncoding: str
    contentSchema: "ContentVocabularyMetaSchema"
    """ Content vocabulary meta-schema. """
