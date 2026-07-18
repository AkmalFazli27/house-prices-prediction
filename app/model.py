from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from .features import engineer_features
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

class HousePriceModel:
    def __init__(self):
        self.preprocessing_pipeline = None
        self.stacking_regressor = None

    def load(self):
        self.preprocessing_pipeline = joblib.load(
            MODEL_DIR / "preprocessing_pipeline.pkl"
        )
        self.stacking_regressor = joblib.load(
            MODEL_DIR / "stacking_regressor.pkl"
        )

    def predict_with_confidence(self, df: pd.DataFrame) -> dict:
        df_featured = engineer_features(df)
        X = self.preprocessing_pipeline.transform(df_featured)

        indiv_log = np.array([est.predict(X) for est in self.stacking_regressor.estimators_])
        y_pred_log = self.stacking_regressor.predict(X)
        pred_value = float(np.exp(y_pred_log[0]))

        indiv_price = np.exp(indiv_log[:, 0])
        std = float(np.std(indiv_price))
        cv = std / pred_value if pred_value > 0 else 0

        confidence = round(max(0, min(100, (1 - cv / 0.25) * 100)))
        lower = round(max(0, pred_value - 1.96 * std), 0)
        upper = round(pred_value + 1.96 * std, 0)

        return {
            "prediction": pred_value,
            "confidence": confidence,
            "std": round(std, 0),
            "lower": lower,
            "upper": upper,
        }
    
    def simple_to_full(self, total_area, lot_area, totrmsabvgrd, bedroomabvgr,
                       overallqual, house_age, garagecars, fireplaces, neighborhood,
                       kitchenqual=None, exterqual=None, centralair=None,
                       bsmtqual=None, lotfrontage=None) -> dict:

        year_built = 2026 - house_age

        bath_map = {
            1: (1, 0, 0, 0),
            2: (1, 1, 0, 0),
            3: (2, 1, 0, 1),
            4: (2, 1, 1, 1),
            5: (3, 1, 1, 1),
        }
        full_bath, half_bath, bsmt_full, bsmt_half = bath_map.get(
            bedroomabvgr, (2, 1, 0, 0)
        )

        return {
            # === From simple form fields ===
            "OverallQual":   overallqual,
            "LotArea":       lot_area,
            "Neighborhood":  neighborhood,
            "BedroomAbvGr":  bedroomabvgr,
            "TotRmsAbvGrd":  totrmsabvgrd,
            "Fireplaces":    fireplaces,
            "GarageCars":    garagecars,
            "LotFrontage":   lotfrontage,
            "KitchenQual":   kitchenqual,
            "ExterQual":     exterqual,
            "CentralAir":    centralair,
            "BsmtQual":      bsmtqual,

            # === engineer_features() needs all DROP_COLS to exist ===
            "YearBuilt":     year_built,
            "YearRemodAdd":  year_built,
            "YrSold":        2026,
            "1stFlrSF":      round(total_area, 2),
            "2ndFlrSF":      0,
            "BsmtFinSF1":    0,
            "BsmtFinSF2":    0,
            "GrLivArea":     round(total_area, 2),
            "TotalBsmtSF":   0,
            "FullBath":      full_bath,
            "HalfBath":      half_bath,
            "BsmtFullBath":  bsmt_full,
            "BsmtHalfBath":  bsmt_half,
            "OpenPorchSF":   0,
            "3SsnPorch":     0,
            "EnclosedPorch": 0,
            "ScreenPorch":   0,
            "WoodDeckSF":    0,
            "GarageArea":    round(garagecars * 250, 2),
        }