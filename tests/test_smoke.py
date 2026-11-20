"""Smoke tests to make sure the package is importable."""

import wastewise


def test_package_imports():
    assert wastewise.__name__ == "wastewise"


def test_package_has_version():
    assert isinstance(wastewise.__version__, str)
    assert wastewise.__version__
