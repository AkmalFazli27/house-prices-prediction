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

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        df_featured = engineer_features(df)
        X = self.preprocessing_pipeline.transform(df_featured)
        y_pred_log = self.stacking_regressor.predict(X)
        return np.exp(y_pred_log)

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