"""Дымовой тест раскладки: пакет из src/ импортируется и знает свою версию."""

import linear_models


def test_package_is_importable_and_has_version() -> None:
    assert linear_models.__version__ != ""
