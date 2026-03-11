"""
Automatically generated file from a JSON schema.
"""

from typing import Any, TypedDict, Union


class JSONSchemaItemD2020(TypedDict, total=False):
    title: str
    description: str
    default: Any
    deprecated: bool
    r""" default: False """

    readOnly: bool
    r""" default: False """

    writeOnly: bool
    r""" default: False """

    examples: list[Any]


MetaDataVocabularyMetaSchema = Union["JSONSchemaItemD2020", bool]
r""" Meta-data vocabulary meta-schema. """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_DEPRECATED_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object deprecated' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object readOnly' """


_META_DATA_VOCABULARY_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
r""" Default value of the field path 'Meta-data vocabulary meta-schema object writeOnly' """
