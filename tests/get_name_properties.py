from typing import TypedDict

from typing_extensions import Required


class ResponseType(TypedDict, total=False):
    """ResponseType."""

    subresource_uris: Required["SubresourceUris"]
    """
    SubresourceUris.

    Required property
    """


class SubresourceUris(TypedDict, total=False):
    """SubresourceUris."""

    feedback: Required[str]
    """ Required property """
