"""Tests for the Kaggle download script (no network, no real credentials)."""

from pathlib import Path

import pytest

from wastewise.data import download
from wastewise.data.download import (
    EXPECTED_FILES,
    KaggleCredentialsError,
    download_dataset,
    find_kaggle_credentials,
    missing_files,
)


@pytest.fixture
def no_credentials(monkeypatch, tmp_path):
    """Isolate the test from any real Kaggle credentials on the machine."""
    for var in ("KAGGLE_API_TOKEN", "KAGGLE_USERNAME", "KAGGLE_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("KAGGLE_CONFIG_DIR", str(tmp_path / "kaggle_cfg"))
    return tmp_path / "kaggle_cfg"


def _touch_expected(dest):
    for name in EXPECTED_FILES:
        (dest / name).write_text("x\n")


class FakeApi:
    def __init__(self, files_to_create):
        self.files_to_create = files_to_create
        self.calls = []

    def dataset_download_files(self, dataset, path, force, quiet, unzip):
        self.calls.append(dataset)
        for name in self.files_to_create:
            (Path(path) / name).write_text("x\n")


def test_find_credentials_none(tmp_path):
    assert find_kaggle_credentials(env={}, home=tmp_path) is None


def test_find_credentials_from_env_token(tmp_path):
    assert find_kaggle_credentials(env={"KAGGLE_API_TOKEN": "t"}, home=tmp_path) == (
        "env:KAGGLE_API_TOKEN"
    )


def test_find_credentials_requires_both_username_and_key(tmp_path):
    assert find_kaggle_credentials(env={"KAGGLE_USERNAME": "u"}, home=tmp_path) is None
    env = {"KAGGLE_USERNAME": "u", "KAGGLE_KEY": "k"}
    assert find_kaggle_credentials(env=env, home=tmp_path) == "env:KAGGLE_USERNAME/KAGGLE_KEY"


def test_find_credentials_from_kaggle_json(tmp_path):
    (tmp_path / ".kaggle").mkdir()
    (tmp_path / ".kaggle" / "kaggle.json").write_text("{}")
    assert find_kaggle_credentials(env={}, home=tmp_path).endswith("kaggle.json")


def test_missing_files_lists_absent_files(tmp_path):
    (tmp_path / EXPECTED_FILES[0]).write_text("x\n")
    assert missing_files(tmp_path) == list(EXPECTED_FILES[1:])


def test_download_without_credentials_raises_clear_error(no_credentials, tmp_path):
    with pytest.raises(KaggleCredentialsError, match="kaggle.json"):
        download_dataset(dest=tmp_path / "raw", api_factory=lambda: pytest.fail("no API call"))


def test_download_skips_when_files_present(no_credentials, tmp_path):
    _touch_expected(tmp_path)
    paths = download_dataset(dest=tmp_path, api_factory=lambda: pytest.fail("no API call"))
    assert [p.name for p in paths] == list(EXPECTED_FILES)


def test_download_calls_api_and_verifies_files(monkeypatch, no_credentials, tmp_path):
    monkeypatch.setenv("KAGGLE_API_TOKEN", "fake")
    api = FakeApi(EXPECTED_FILES)
    download_dataset(dataset="owner/name", dest=tmp_path, api_factory=lambda: api)
    assert api.calls == ["owner/name"]
    assert missing_files(tmp_path) == []


def test_download_reports_unexpected_dataset_contents(monkeypatch, no_credentials, tmp_path):
    monkeypatch.setenv("KAGGLE_API_TOKEN", "fake")
    api = FakeApi(["something_else.csv"])
    with pytest.raises(FileNotFoundError, match="something_else.csv"):
        download_dataset(dest=tmp_path, api_factory=lambda: api)


def test_main_returns_error_code_without_credentials(no_credentials, tmp_path, capsys):
    assert download.main(["--dest", str(tmp_path / "raw")]) == 1
    assert "Kaggle credentials not found" in capsys.readouterr().err
