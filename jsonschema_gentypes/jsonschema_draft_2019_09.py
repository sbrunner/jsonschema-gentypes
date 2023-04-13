"""
Automatically generated file from a JSON schema.
"""


from typing import Any, Dict, List, TypedDict, Union

CoreAndValidationSpecificationsMetaSchema = Union["_CoreAndValidationSpecificationsMetaSchemaObject", bool]
""" Core and Validation specifications meta-schema. """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: Dict[str, Any] = {}
""" Default value of the field path 'Core and Validation specifications meta-schema object definitions' """


_CORE_AND_VALIDATION_SPECIFICATIONS_META_SCHEMA_OBJECT_DEPENDENCIES_ADDITIONALPROPERTIES_ANYOF1_DEFAULT: List[
    Any
] = []
""" Default value of the field path 'Core and Validation specifications meta-schema object dependencies additionalProperties anyof1' """


class _CoreAndValidationSpecificationsMetaSchemaObject(TypedDict, total=False):
    definitions: Dict[str, "CoreAndValidationSpecificationsMetaSchema"]
    """
    $comment: While no longer an official keyword as it is replaced by $defs, this keyword is retained in the meta-schema to prevent incompatible extensions as it remains in common use.
    default:
      {}
    """

    dependencies: Dict[
        str, Union["CoreAndValidationSpecificationsMetaSchema", "_MetaValidationNumberSignDefsStringarray"]
    ]
    """ $comment: "dependencies" is no longer a keyword, but schema authors should avoid redefining it to facilitate a smooth transition to "dependentSchemas" and "dependentRequired" """


_META_VALIDATION_NUMBER_SIGN___DEFS_STRINGARRAY_DEFAULT: List[Any] = []
""" Default value of the field path 'meta validation# $defs stringArray' """


_MetaValidationNumberSignDefsStringarray = List[str]
"""
uniqueItems: True
default:
  []
"""
