# Detailed Mode Page — Omah.AI

## Objective

Build a `/detail` page for the Omah.AI app that accepts all 79 raw property features from the Ames Housing dataset, organized into 9 logical groups with user-friendly display names and descriptive dropdown values. Matches the existing Omah.AI design language (pure CSS, Jinja2 templates, Material Symbols).

## Layout

- **Left sidebar** (sticky): 9 group items with icons, scroll-spy highlighting (active section tracks viewport position)
- **Right content**: single scrollable page with all 9 sections visible; each section is a card with group heading and field grid
- Same navbar/footer pattern as `index.html` and `simple.html`

## 9 Feature Groups

| # | Group | Fields | Type Count |
|---|-------|--------|------------|
| 1 | Lot & Location | MSSubClass, MSZoning, LotFrontage, LotArea, Street, Alley, LotShape, LandContour, Utilities, LotConfig, LandSlope, Neighborhood, Condition1, Condition2 | 14 (10 select, 4 number) |
| 2 | Building Structure | BldgType, HouseStyle, OverallQual, OverallCond, YearBuilt, YearRemodAdd | 6 (2 select, 2 slider, 2 number) |
| 3 | Exterior & Foundation | RoofStyle, RoofMatl, Exterior1st, Exterior2nd, MasVnrType, MasVnrArea, ExterQual, ExterCond, Foundation | 9 (8 select, 1 number) |
| 4 | Basement | BsmtQual, BsmtCond, BsmtExposure, BsmtFinType1, BsmtFinSF1, BsmtFinType2, BsmtFinSF2, BsmtUnfSF, TotalBsmtSF | 9 (4 select, 5 number) |
| 5 | Interior & Rooms | 1stFlrSF, 2ndFlrSF, LowQualFinSF, GrLivArea, BsmtFullBath, BsmtHalfBath, FullBath, HalfBath, BedroomAbvGr, KitchenAbvGr, KitchenQual, TotRmsAbvGrd, Functional, Fireplaces, FireplaceQu | 15 (3 select, 12 number) |
| 6 | Heating & Electrical | Heating, HeatingQC, CentralAir, Electrical | 4 (4 select) |
| 7 | Garage | GarageType, GarageYrBlt, GarageFinish, GarageCars, GarageArea, GarageQual, GarageCond | 8 (5 select, 2 number, 1 year) |
| 8 | Outdoor Features | PavedDrive, WoodDeckSF, OpenPorchSF, EnclosedPorch, 3SsnPorch, ScreenPorch, PoolArea, PoolQC, Fence, MiscFeature, MiscVal | 12 (5 select, 7 number) |
| 9 | Sale Information | MoSold, YrSold, SaleType, SaleCondition | 5 (2 select, 2 number, 1 year) |

## Feature Display Names

All feature labels use user-friendly names (e.g., "Dwelling Type" not "MSSubClass", "Zoning Classification" not "MSZoning").

## Dropdown Options

All select options use full descriptive text from `data/data_description.txt`:
- "Gravel" not "Grvl", "Residential Low Density" not "RL", "Excellent (100+ inches)" not "Ex"
- Each `<option>` value stores the raw code (e.g., `value="RL"`), display text shows the description

## New Files

- **`app/feature_data.py`** — Python dict defining all groups, fields, display names, input types, and dropdown options. Single source of truth.
- **`app/templates/detail.html`** — Jinja2 template that loops over `feature_data` to render sidebar + form sections. Includes scroll-spy JS.

## Modified Files

- **`app/main.py`** — add `GET /detail` and `POST /detail` routes
- **`app/static/css/style.css`** — add detail page classes (sidebar, scroll-spy, form-grid, field variants)

## Data Flow

1. User fills form → `POST /detail` with form-encoded data
2. `main.py` constructs `HouseInput` Pydantic model from form data
3. `HousePriceModel.predict()` runs `engineer_features()` → preprocessing pipeline → stacking regressor
4. Result is `np.exp()` of log-transformed prediction → renders result page

## Consistency

- Same navbar + footer as `index.html` and `simple.html`
- Same CSS design tokens (fonts, colors, spacing)
- Same Material Symbols icon set
- Jinja2 templating with FastAPI
