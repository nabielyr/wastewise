"""Tests for the typed CSV loaders and the merge, using hand-made fixture files."""

from pathlib import Path

import pandas as pd
import pytest

from wastewise.data.load import (
    CENTER_INFO_DTYPES,
    MEAL_INFO_DTYPES,
    TEST_DTYPES,
    TRAIN_DTYPES,
    load_center_info,
    load_interim_merged,
    load_meal_info,
    load_merged_train,
    load_test,
    load_train,
    merge_orders,
    read_csv_typed,
    save_merged_train,
)

FIXTURE_RAW = Path(__file__).parent / "fixtures" / "raw"


@pytest.mark.parametrize(
    ("loader", "dtypes", "n_rows"),
    [
        (load_train, TRAIN_DTYPES, 6),
        (load_test, TEST_DTYPES, 2),
        (load_center_info, CENTER_INFO_DTYPES, 2),
        (load_meal_info, MEAL_INFO_DTYPES, 2),
    ],
)
def test_loaders_apply_explicit_dtypes(loader, dtypes, n_rows):
    df = loader(FIXTURE_RAW)
    assert len(df) == n_rows
    assert list(df.columns) == list(dtypes)
    assert df.dtypes.astype(str).to_dict() == dtypes


def test_load_train_keeps_values():
    df = load_train(FIXTURE_RAW)
    first = df.iloc[0]
    assert first["id"] == 1000001
    assert first["checkout_price"] == pytest.approx(136.83)
    assert first["num_orders"] == 177
    assert df["num_orders"].sum() == 177 + 270 + 95 + 250 + 243 + 108


def test_missing_file_raises_with_hint(tmp_path):
    with pytest.raises(FileNotFoundError, match="make data"):
        load_train(tmp_path)


def test_unexpected_columns_raise(tmp_path):
    path = tmp_path / "meal_info.csv"
    path.write_text("meal_id,category,price\n1885,Beverages,10\n")
    with pytest.raises(ValueError, match=r"missing=\['cuisine'\].*extra=\['price'\]"):
        read_csv_typed(path, MEAL_INFO_DTYPES)


def test_columns_are_reordered_to_schema(tmp_path):
    path = tmp_path / "meal_info.csv"
    path.write_text("cuisine,meal_id,category\nThai,1885,Beverages\n")
    df = read_csv_typed(path, MEAL_INFO_DTYPES)
    assert list(df.columns) == ["meal_id", "category", "cuisine"]


def test_merge_keeps_row_count_and_attaches_attributes():
    merged = load_merged_train(FIXTURE_RAW)
    assert len(merged) == len(load_train(FIXTURE_RAW))
    assert merged.isna().sum().sum() == 0

    row = merged.loc[merged["id"] == 1000003].iloc[0]
    assert row["center_type"] == "TYPE_B"
    assert row["region_code"] == 34
    assert row["category"] == "Beverages"
    assert row["cuisine"] == "Thai"


def test_merge_preserves_categorical_dtypes():
    merged = load_merged_train(FIXTURE_RAW)
    for col in ("center_type", "category", "cuisine"):
        assert isinstance(merged[col].dtype, pd.CategoricalDtype)


def test_merge_raises_on_unknown_center():
    orders = load_train(FIXTURE_RAW)
    centers = load_center_info(FIXTURE_RAW)
    meals = load_meal_info(FIXTURE_RAW)
    with pytest.raises(ValueError, match="center_id"):
        merge_orders(orders, centers[centers["center_id"] != 20], meals)


def test_merge_rejects_duplicate_info_rows():
    orders = load_train(FIXTURE_RAW)
    centers = load_center_info(FIXTURE_RAW)
    meals = load_meal_info(FIXTURE_RAW)
    with pytest.raises(pd.errors.MergeError):
        merge_orders(orders, centers, pd.concat([meals, meals]))


def test_save_merged_train_roundtrip(tmp_path):
    out_path = save_merged_train(FIXTURE_RAW, tmp_path)
    assert out_path.suffix == ".parquet"

    original = load_merged_train(FIXTURE_RAW)
    reloaded = load_interim_merged(tmp_path)
    pd.testing.assert_frame_equal(reloaded, original)


def test_load_interim_merged_missing_file_hint(tmp_path):
    with pytest.raises(FileNotFoundError, match="make interim"):
        load_interim_merged(tmp_path)
