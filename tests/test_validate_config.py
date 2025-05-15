from pathlib import Path

import pytest

from jsonschema_gentypes.cli import validate_config


def test_validate_good_config() -> None:
    validate_config(Path(__file__).parent / "good-config.yaml")


def test_validate_bad_config() -> None:
    with pytest.raises(SystemExit):
        validate_config(Path(__file__).parent / "bad-config.yaml")
