from contextlib import asynccontextmanager

import pandas as pd
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .feature_data import FEATURE_GROUPS
from pydantic import ValidationError
from .model import HousePriceModel
from .schemas import (
    BatchHouseInput,
    BatchPredictionOutput,
    HouseInput,
    PredictionOutput,
    SimpleHouseInput,
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))

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

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/simple", response_class=HTMLResponse)
def simple_form(request: Request):
    return TEMPLATES.TemplateResponse(request, "simple.html")

@app.post("/simple", response_class=HTMLResponse)
async def simple_predict(request: Request):
    form_data = await request.form()
    form = dict(form_data)
    for k, v in form.items():
        if v == '':
            form[k] = None
    try:
        simple = SimpleHouseInput(**form)
    except ValidationError as e:
        return TEMPLATES.TemplateResponse(request, "simple.html", {
            "error": f"Invalid input: {e.errors()[0]['msg']}",
            "form_data": form
        })
    full = model.simple_to_full(
        total_area=simple.total_area,
        lot_area=simple.lot_area,
        totrmsabvgrd=simple.totrmsabvgrd,
        bedroomabvgr=simple.bedroomabvgr,
        overallqual=simple.overallqual,
        house_age=simple.house_age,
        garagecars=simple.garagecars,
        fireplaces=simple.fireplaces,
        neighborhood=simple.neighborhood,
        kitchenqual=simple.kitchenqual,
        exterqual=simple.exterqual,
        centralair=simple.centralair,
        bsmtqual=simple.bsmtqual,
        lotfrontage=simple.lotfrontage,
    )
    df = pd.DataFrame([full])
    try:
        result = model.predict_with_confidence(df)
    except Exception as e:
        logger.error(f"Simple prediction failed: {e}", exc_info=True)
        return TEMPLATES.TemplateResponse(request, "simple.html", {
            "error": "Prediction failed. Please check your inputs.",
            "form_data": form
        })
    return TEMPLATES.TemplateResponse(request, "simple.html", {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "lower": result["lower"],
        "upper": result["upper"],
        "form_data": form
    })

@app.get("/detail", response_class=HTMLResponse)
def detail_form(request: Request):
    return TEMPLATES.TemplateResponse(request, "detail.html", {
        "groups": FEATURE_GROUPS,
        "form_data": {}
    })

@app.post("/detail", response_class=HTMLResponse)
async def detail_predict(request: Request):
    form_data = await request.form()
    form = dict(form_data)
    for k, v in form.items():
        if v == '':
            form[k] = None
    try:
        house = HouseInput(**form)
    except ValidationError as e:
        return TEMPLATES.TemplateResponse(request, "detail.html", {
            "groups": FEATURE_GROUPS,
            "error": f"Invalid input: {e.errors()[0]['msg']}",
            "form_data": form
        })
    df = pd.DataFrame([house.model_dump(by_alias=True)])
    try:
        result = model.predict_with_confidence(df)
    except Exception as e:
        logger.error(f"Detail prediction failed: {e}", exc_info=True)
        return TEMPLATES.TemplateResponse(request, "detail.html", {
            "groups": FEATURE_GROUPS,
            "error": "Prediction failed. Please check your inputs.",
            "form_data": form
        })
    return TEMPLATES.TemplateResponse(request, "detail.html", {
        "groups": FEATURE_GROUPS,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "lower": result["lower"],
        "upper": result["upper"],
        "form_data": form
    })

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput)
def predict_one(house: HouseInput):
    logger.info(f"Predict request: MSSubClass={house.MSSubClass}, "
                f"OverallQual={house.OverallQual}, LotArea={house.LotArea}")

    df = pd.DataFrame([house.model_dump(by_alias=True)])

    try:
        result = model.predict_with_confidence(df)
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed")
    
    logger.info(f"Prediction result: ${result['prediction']:.2f} (confidence: {result['confidence']}%)")
    return PredictionOutput(
        prediction=result["prediction"],
        confidence=result["confidence"],
        lower=result["lower"],
        upper=result["upper"],
    )

@app.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(batch: BatchHouseInput):
    df = pd.DataFrame([h.model_dump(by_alias=True) for h in batch.houses])
    
    try:
        preds = model.predict(df)
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Batch prediction failed")
    
    logger.info(f"Batch predict result: {len(preds)} predictions")
    return BatchPredictionOutput(predictions=preds.tolist())

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )