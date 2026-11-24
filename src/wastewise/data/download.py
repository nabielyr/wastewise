"""Download the Food Demand Forecasting dataset from Kaggle into data/raw/.

Usage:
    python -m wastewise.data.download [--dataset OWNER/NAME] [--dest DIR] [--force]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

from wastewise.config import (
    CENTER_INFO_FILE,
    KAGGLE_DATASET,
    MEAL_INFO_FILE,
    RAW_DATA_DIR,
    TEST_FILE,
    TRAIN_FILE,
)

EXPECTED_FILES = (TRAIN_FILE, CENTER_INFO_FILE, MEAL_INFO_FILE, TEST_FILE)

CREDENTIALS_HELP = """\
Kaggle download failed and no credentials were found. Public datasets usually
download anonymously; if that fails, set up ONE of the following and run again:

  1. Legacy API key file: download kaggle.json from https://www.kaggle.com/settings
     ("Create Legacy API Key") and save it to {kaggle_json}
  2. API token file: save the token from https://www.kaggle.com/settings
     ("Generate New Token") to {access_token}
  3. Environment variable KAGGLE_API_TOKEN=<token>
  4. Environment variables KAGGLE_USERNAME=<user> and KAGGLE_KEY=<key>

Never commit these credentials to git.
"""


class KaggleCredentialsError(RuntimeError):
    """Raised when the dataset cannot be downloaded with or without credentials."""


def kaggle_config_dir(env: Mapping[str, str] | None = None, home: Path | None = None) -> Path:
    """Return the directory where the Kaggle client looks for credential files."""
    env = os.environ if env is None else env
    if env.get("KAGGLE_CONFIG_DIR"):
        return Path(env["KAGGLE_CONFIG_DIR"])
    return (home or Path.home()) / ".kaggle"


def find_kaggle_credentials(
    env: Mapping[str, str] | None = None, home: Path | None = None
) -> str | None:
    """Return a short description of the credential source found, or None if there is none."""
    env = os.environ if env is None else env
    if env.get("KAGGLE_API_TOKEN"):
        return "env:KAGGLE_API_TOKEN"
    if env.get("KAGGLE_USERNAME") and env.get("KAGGLE_KEY"):
        return "env:KAGGLE_USERNAME/KAGGLE_KEY"
    config_dir = kaggle_config_dir(env, home)
    for name in ("access_token", "kaggle.json"):
        if (config_dir / name).is_file():
            return f"file:{config_dir / name}"
    return None


def credentials_help() -> str:
    """Return setup instructions pointing at this machine's Kaggle config directory."""
    config_dir = kaggle_config_dir()
    return CREDENTIALS_HELP.format(
        kaggle_json=config_dir / "kaggle.json", access_token=config_dir / "access_token"
    )


def missing_files(dest: Path, expected: tuple[str, ...] = EXPECTED_FILES) -> list[str]:
    """Return the expected raw files that are not present in ``dest``."""
    return [name for name in expected if not (dest / name).is_file()]


def _authenticated_api():
    """Create an authenticated Kaggle API client.

    Imported lazily because ``import kaggle`` tries to authenticate at import time.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    try:
        api.authenticate()
    except SystemExit as exc:  # the client calls exit(1) on auth failure
        raise KaggleCredentialsError(credentials_help()) from exc
    return api


def _download_anonymously(dataset: str, dest: Path, force: bool) -> None:
    """Download a public dataset through the Kaggle CLI without credentials.

    The Kaggle client only allows logged-out access when it runs as the CLI
    (``python -m kaggle``), not when imported as a library, so this shells out.
    """
    cmd = [sys.executable, "-m", "kaggle", "datasets", "download", dataset]
    cmd += ["-p", str(dest), "--unzip"]
    if force:
        cmd.append("--force")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise KaggleCredentialsError(
            credentials_help() + f"\nAnonymous download exited with code {result.returncode}."
        )


def download_dataset(
    dataset: str = KAGGLE_DATASET,
    dest: Path = RAW_DATA_DIR,
    force: bool = False,
    api_factory=None,
    anonymous_downloader=None,
) -> list[Path]:
    """Download and unzip ``dataset`` into ``dest`` and return the expected file paths.

    Skips the download when all expected files already exist, unless ``force`` is set.
    Uses the authenticated API when credentials are configured, otherwise tries an
    anonymous download (enough for public datasets). Raises KaggleCredentialsError if
    both fail and FileNotFoundError if the dataset lacks the expected files.
    """
    api_factory = api_factory or _authenticated_api
    anonymous_downloader = anonymous_downloader or _download_anonymously
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    if not force and not missing_files(dest):
        print(f"All raw files already present in {dest}, skipping download (use --force).")
        return [dest / name for name in EXPECTED_FILES]

    source = find_kaggle_credentials()
    if source is None:
        print(f"No Kaggle credentials found, downloading '{dataset}' anonymously to {dest} ...")
        anonymous_downloader(dataset, dest, force)
    else:
        print(f"Downloading Kaggle dataset '{dataset}' to {dest} (credentials: {source}) ...")
        api = api_factory()
        api.dataset_download_files(dataset, path=str(dest), force=force, quiet=False, unzip=True)

    missing = missing_files(dest)
    if missing:
        present = sorted(p.name for p in dest.iterdir() if p.name != ".gitkeep")
        raise FileNotFoundError(
            f"Dataset '{dataset}' is missing expected files {missing}. "
            f"Files found in {dest}: {present}"
        )

    print("Download complete: " + ", ".join(EXPECTED_FILES))
    return [dest / name for name in EXPECTED_FILES]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the raw dataset from Kaggle.")
    parser.add_argument("--dataset", default=KAGGLE_DATASET, help="Kaggle slug OWNER/NAME")
    parser.add_argument("--dest", type=Path, default=RAW_DATA_DIR, help="Output directory")
    parser.add_argument("--force", action="store_true", help="Re-download even if files exist")
    args = parser.parse_args(argv)

    try:
        download_dataset(args.dataset, args.dest, force=args.force)
    except KaggleCredentialsError as exc:
        print(exc, file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
