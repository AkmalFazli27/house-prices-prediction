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