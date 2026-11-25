"""Typed loaders for the raw Food Demand Forecasting CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from wastewise.config import (
    CENTER_INFO_FILE,
    MEAL_INFO_FILE,
    RAW_DATA_DIR,
    TEST_FILE,
    TRAIN_FILE,
)

# Explicit dtypes per file. IDs and codes are identifiers, not quantities, but stay
# integer here; encoding happens in feature engineering. Prices keep float64 precision.
ORDER_DTYPES: dict[str, str] = {
    "id": "int64",
    "week": "int16",
    "center_id": "int16",
    "meal_id": "int16",
    "checkout_price": "float64",
    "base_price": "float64",
    "emailer_for_promotion": "int8",
    "homepage_featured": "int8",
}
TRAIN_DTYPES: dict[str, str] = {**ORDER_DTYPES, "num_orders": "int32"}
TEST_DTYPES: dict[str, str] = dict(ORDER_DTYPES)

CENTER_INFO_DTYPES: dict[str, str] = {
    "center_id": "int16",
    "city_code": "int16",
    "region_code": "int16",
    "center_type": "category",
    "op_area": "float64",
}

MEAL_INFO_DTYPES: dict[str, str] = {
    "meal_id": "int16",
    "category": "category",
    "cuisine": "category",
}


def read_csv_typed(path: Path, dtypes: dict[str, str]) -> pd.DataFrame:
    """Read ``path`` with the given dtypes, requiring exactly the expected columns.

    Raises FileNotFoundError if the file is missing and ValueError if columns differ.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"{path} not found. Run `make data` to download the dataset.")

    header = pd.read_csv(path, nrows=0).columns.tolist()
    missing = [col for col in dtypes if col not in header]
    extra = [col for col in header if col not in dtypes]
    if missing or extra:
        raise ValueError(f"{path.name}: unexpected columns (missing={missing}, extra={extra})")

    return pd.read_csv(path, dtype=dtypes)[list(dtypes)]


def load_train(raw_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """Load weekly orders per center and meal, including the ``num_orders`` target."""
    return read_csv_typed(Path(raw_dir) / TRAIN_FILE, TRAIN_DTYPES)


def load_test(raw_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """Load the competition test file (no target, not used for evaluation)."""
    return read_csv_typed(Path(raw_dir) / TEST_FILE, TEST_DTYPES)


def load_center_info(raw_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """Load fulfilment center attributes (city, region, type, operating area)."""
    return read_csv_typed(Path(raw_dir) / CENTER_INFO_FILE, CENTER_INFO_DTYPES)


def load_meal_info(raw_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """Load meal attributes (category and cuisine)."""
    return read_csv_typed(Path(raw_dir) / MEAL_INFO_FILE, MEAL_INFO_DTYPES)
