"""Automatically generated file from a JSON schema."""

from typing import Any, TypedDict, Union


class JSONSchemaItemD2020(TypedDict, total=False):
    title: str
    description: str
    default: Any
    deprecated: bool
    """ default: False """

    readOnly: bool
    """ default: False """

    writeOnly: bool
    """ default: False """

    examples: list[Any]


MetaDataVocabularyMetaSchema = Union["JSONSchemaItemD2020", bool]
""" Meta-data vocabulary meta-schema. """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object deprecated' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object readOnly' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
""" Default value of the field path 'Meta-data vocabulary meta-schema object writeOnly' """
