"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, TypedDict, Union

CoreAndValidationSpecificationsMetaSchema = Union["_CoreAndValidationSpecificationsMetaSchemaObject", bool]
"""
Core and Validation specifications meta-schema.

$comment: This meta-schema also defines keywords that have appeared in previous drafts in order to prevent incompatible extensions as they remain in common use.
"""


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core and Validation specifications meta-schema object definitions' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEPENDENCIES_ADDITIONALPROPERTIES_ANYOF1_DEFAULT: List[
    Any
] = []
""" Default value of the field path 'Core and Validation specifications meta-schema object dependencies additionalProperties anyof1' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEPENDENCIES_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core and Validation specifications meta-schema object dependencies' """


# $comment: This meta-schema also defines keywords that have appeared in previous drafts in order to prevent incompatible extensions as they remain in common use.
_CoreAndValidationSpecificationsMetaSchemaObject = TypedDict(
    "_CoreAndValidationSpecificationsMetaSchemaObject",
    {
        # $comment: "definitions" has been replaced by "$defs".
        # deprecated: True
        # default:
        #   {}
        "definitions": Dict[str, "CoreAndValidationSpecificationsMetaSchema"],
        # $comment: "dependencies" has been split and replaced by "dependentSchemas" and "dependentRequired" in order to serve their differing semantics.
        # deprecated: True
        # default:
        #   {}
        "dependencies": Dict[
            str,
            Union["CoreAndValidationSpecificationsMetaSchema", "_MetaValidationNumberSignDefsStringarray"],
        ],
        "$recursiveAnchor": "_MetaCoreNumberSignDefsAnchorstring",
        "$recursiveRef": "_MetaCoreNumberSignDefsUrireferencestring",
    },
    total=False,
)


_META_VALIDATION_NUMBER_SIGN___DEFS_STRINGARRAY_DEFAULT: List[Any] = []
""" Default value of the field path 'meta validation# $defs stringArray' """


_MetaCoreNumberSignDefsAnchorstring = str
""" pattern: ^[A-Za-z_][-A-Za-z0-9._]*$ """


_MetaCoreNumberSignDefsUrireferencestring = str
""" format: uri-reference """


_MetaValidationNumberSignDefsStringarray = List[str]
"""
uniqueItems: True
default:
  []
"""
