from contextlib import asynccontextmanager

import pandas as pd
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException

from .model import HousePriceModel
from .schemas import (
    BatchHouseInput,
    BatchPredictionOutput,
    HouseInput,
    PredictionOutput,
)

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

model = HousePriceModel()

@asynccontextmanager
async def lifespan(app: FastAPI):
    model.load()
    yield

app = FastAPI(title="House Prediction API", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput)
def predict_one(house: HouseInput):
    logger.info(f"Predict request: MSSubClass={house.MSSubClass}, "
                f"OverallQual={house.OverallQual}, LotArea={house.LotArea}")

    df = pd.DataFrame([house.model_dump(by_alias=True)])

    try:
        pred = model.predict(df)
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed")
    
    result = float(pred[0])
    logger.info(f"Prediction result: ${result:.2f}")
    return PredictionOutput(prediction=result)

@app.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(batch: BatchHouseInput):
    df = pd.DataFrame([h.model_dump(by_alias=True) for h in batch.houses])
    preds = model.predict(df)
    return BatchPredictionOutput(predictions=preds.tolist())
