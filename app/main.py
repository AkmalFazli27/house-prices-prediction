from contextlib import asynccontextmanager

import pandas as pd
import logging
from pathlib import Path
from fastapi import FastAPI

from .model import HousePriceModel
from .schemas import (
    BatchHouseInput,
    BatchPredictionOutput,
    HouseInput,
    PredictionOutput,
)

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
    df = pd.DataFrame([house.model_dump(by_alias=True)])
    pred = model.predict(df)
    return PredictionOutput(prediction=float(pred[0]))

@app.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(batch: BatchHouseInput):
    df = pd.DataFrame([h.model_dump(by_alias=True) for h in batch.houses])
    preds = model.predict(df)
    return BatchPredictionOutput(predictions=preds.tolist())

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