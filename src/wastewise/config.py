"""Central configuration: project paths and global constants."""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
APP_DATA_DIR = DATA_DIR / "app"

MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCS_DIR = PROJECT_ROOT / "docs"

# Dataset
# Kaggle slug for the Food Demand Forecasting dataset (Genpact / Analytics Vidhya).
# Verified: public, downloadable anonymously (see docs/decisions.md D-005).
KAGGLE_DATASET = "kannanaikkal/food-demand-forecasting"

TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"
CENTER_INFO_FILE = "fulfilment_center_info.csv"
MEAL_INFO_FILE = "meal_info.csv"

TARGET_COL = "num_orders"
SERIES_KEYS = ("center_id", "meal_id")
TIME_COL = "week"

# Modeling
RANDOM_SEED = 42
FORECAST_HORIZON_WEEKS = 1
HOLDOUT_WEEKS = 10
