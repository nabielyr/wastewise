"""Tests for the central config module."""

from wastewise import config


def test_project_root_contains_pyproject():
    assert (config.PROJECT_ROOT / "pyproject.toml").is_file()


def test_data_dirs_are_under_project_root():
    for path in (
        config.RAW_DATA_DIR,
        config.INTERIM_DATA_DIR,
        config.PROCESSED_DATA_DIR,
        config.APP_DATA_DIR,
        config.MODELS_DIR,
        config.FIGURES_DIR,
    ):
        assert path.is_relative_to(config.PROJECT_ROOT)


def test_holdout_is_positive():
    assert config.HOLDOUT_WEEKS > 0
    assert config.FORECAST_HORIZON_WEEKS > 0
