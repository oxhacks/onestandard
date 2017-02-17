"""Test the onestandard models."""

import pytest

from onestandard import models


def test_standard_bootstrap():
    """Ensure the object initializes appropriately."""
    title = 'test_standard'
    content_type = 'tag'
    standard = models.Standard(title, content_type)
    assert standard.title == title
    assert standard.content_type == content_type
    assert len(standard.guid) > 0


def test_with_guid():
    """Ensure an object initializes properly with a predefined guid."""
    title = 'test_standard'
    content_type = 'tag'
    guid = "0200730f-091c-4cbb-a799-7f2209ace34f"
    standard = models.Standard(title, content_type, guid=guid)
    assert standard.guid == guid
