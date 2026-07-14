from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from .features import engineer_features

class HousePriceModel:
    def __init__(self):
        self.preprocessing_pipeline = None
        self.stacking_regressor = None

    MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
    
    def load(self):
        self.preprocessing_pipeline = joblib.load(
            self.MODEL_DIR / "preprocessing_pipeline.pkl"
        )
        self.stacking_regressor = joblib.load(
            self.MODEL_DIR / "stacking_regressor.pkl"
        )

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        df_featured = engineer_features(df)
        X = self.preprocessing_pipeline.transform(df_featured)
        y_pred_log = self.stacking_regressor.predict(X)
        return np.exp(y_pred_log)