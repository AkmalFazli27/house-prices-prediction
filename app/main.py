from contextlib import asynccontextmanager

import pandas as pd
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