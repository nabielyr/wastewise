# Data Dictionary

Source: Kaggle dataset [`kannanaikkal/food-demand-forecasting`](https://www.kaggle.com/datasets/kannanaikkal/food-demand-forecasting)
(license DbCL-1.0), originally from the Genpact / Analytics Vidhya "Food Demand Forecasting" hackathon.
Weekly orders of a meal delivery company with several fulfilment centers.

All ranges and counts below were computed from the raw files on 2026-11-26.
Dtypes are the ones applied by `src/wastewise/data/load.py`.
Column descriptions marked "(per source)" come from the original competition description and cannot be
verified from the data itself.

## Files

| File | Rows | Columns | Used for |
|---|---:|---:|---|
| `train.csv` | 456,548 | 9 | Modeling and evaluation (time-based holdout) |
| `fulfilment_center_info.csv` | 77 | 5 | Center attributes, joined on `center_id` |
| `meal_info.csv` | 51 | 3 | Meal attributes, joined on `meal_id` |
| `test.csv` | 32,573 | 8 | Not used for evaluation (no `num_orders`) |
| `sample_submission.csv` | | | Not used |

Grain of `train.csv`: one row per (`week`, `center_id`, `meal_id`). There are no duplicate keys and no
missing values in any file. 3,597 distinct center-meal combinations appear in train.

## `train.csv` / `test.csv`

| Column | Dtype | Unit | Range (train) | Description and notes |
|---|---|---|---|---|
| `id` | int64 | none | 1,000,000 to 1,499,999 | Row identifier. Unique, carries no information; dropped for modeling. |
| `week` | int16 | week index | 1 to 145 (test: 146 to 155) | Sequential week number. No calendar dates are given, so seasonality can only be inferred from the index. |
| `center_id` | int16 | none | 10 to 186, 77 unique | Fulfilment center identifier. Join key to center info. |
| `meal_id` | int16 | none | 1062 to 2956, 51 unique | Meal identifier. Join key to meal info. |
| `checkout_price` | float64 | price unit | 2.97 to 866.27 | Final price paid, including discount, taxes and delivery charges (per source). Currency is not stated: report as "price units", never Rupiah. |
| `base_price` | float64 | price unit | 55.35 to 866.27 | Base price of the meal (per source). Same unknown currency. |
| `emailer_for_promotion` | int8 | flag 0/1 | 8.1% of rows = 1 | Meal promoted by email that week. Known before the week starts. |
| `homepage_featured` | int8 | flag 0/1 | 10.9% of rows = 1 | Meal featured on the homepage that week. Known before the week starts. |
| `num_orders` | int32 | orders (count) | 13 to 24,299; median 136, mean 261.9 | **Target.** Orders for that meal at that center in that week. Train only. |

Notes:
- `checkout_price > base_price` in 116,101 rows (25.4%), so `base_price - checkout_price` ("discount")
  is negative for a quarter of the data. Feature engineering must handle negative discounts.
- The smallest `num_orders` is 13 and there are no zeros. Weeks without orders are probably absent rather
  than recorded as 0; series completeness is checked in EDA step 2.8.
- `num_orders` is strongly right-skewed (mean well above median); target distribution is analysed in 2.3.

## `fulfilment_center_info.csv`

| Column | Dtype | Unit | Range | Description and notes |
|---|---|---|---|---|
| `center_id` | int16 | none | 10 to 186, 77 unique | Primary key. Every `center_id` in train has a row here. |
| `city_code` | int16 | none | 456 to 713, 51 unique | Anonymised city code. A label, not a number. |
| `region_code` | int16 | none | 23 to 93, 8 unique | Anonymised region code. A label, not a number. |
| `center_type` | category | none | TYPE_A (43), TYPE_C (19), TYPE_B (15) | Anonymised center type. |
| `op_area` | float64 | area (unit unverified) | 0.9 to 7.0 | Operating area of the center. Described as km² by the source; the data does not confirm the unit. |

## `meal_info.csv`

| Column | Dtype | Unit | Range | Description and notes |
|---|---|---|---|---|
| `meal_id` | int16 | none | 1062 to 2956, 51 unique | Primary key. Every `meal_id` in train has a row here. |
| `category` | category | none | 14 values | Beverages (12 meals); Biryani, Desert, Extras, Fish, Other Snacks, Pasta, Pizza, Rice Bowl, Salad, Sandwich, Seafood, Soup, Starters (3 meals each). "Desert" is spelled as in the source. |
| `cuisine` | category | none | 4 values | Thai (15 meals), Continental (12), Indian (12), Italian (12). |

## Merged dataset

`load_merged_train()` left-joins train with center and meal info: 456,548 rows x 15 columns, no nulls.
Column order: the 9 train columns, then `city_code, region_code, center_type, op_area`, then
`category, cuisine`.

## What the data does not contain

- **No waste, stock or preparation quantities.** Waste is estimated with an inventory policy simulation
  (Phase 8), not measured.
- **No calendar dates, holidays or weather.** Only the week index.
- **No currency or cost data.** Ingredient cost and portion weight used in the waste cost estimate are
  configurable assumptions, documented in `docs/decisions.md` when they are introduced.
