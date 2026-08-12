# Copyright (c) 2021-2026, Camptocamp SA
from typing import Required, TypedDict


class ResponseType(TypedDict, total=False):
    r"""ResponseType."""

    subresource_uris: Required["SubresourceUris"]
    r"""
    SubresourceUris.

    Required property
    """


class SubresourceUris(TypedDict, total=False):
    r"""SubresourceUris."""

    feedback: Required[str]
    r""" Required property """
