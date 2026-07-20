from contextlib import asynccontextmanager
import secrets

import pandas as pd
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .feature_data import FEATURE_GROUPS
from pydantic import ValidationError
from .model import HousePriceModel
from .schemas import (
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
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return TEMPLATES.TemplateResponse(request, "index.html")

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return TEMPLATES.TemplateResponse(request, "about.html")

@app.get("/simple", response_class=HTMLResponse)
def simple_form(request: Request):
    ctx = {}
    pred = request.session.pop("simple_prediction", None)
    err = request.session.pop("simple_error", None)
    form_data = request.session.pop("simple_form_data", None)
    if pred:
        ctx["prediction"] = pred["prediction"]
        ctx["confidence"] = pred["confidence"]
        ctx["lower"] = pred["lower"]
        ctx["upper"] = pred["upper"]
    if err:
        ctx["error"] = err
    if form_data:
        ctx["form_data"] = form_data
    return TEMPLATES.TemplateResponse(request, "simple.html", ctx)

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
        request.session["simple_error"] = f"Invalid input: {e.errors()[0]['msg']}"
        request.session["simple_form_data"] = form
        return RedirectResponse(url="/simple", status_code=303)
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
        request.session["simple_error"] = "Prediction failed. Please check your inputs."
        request.session["simple_form_data"] = form
        return RedirectResponse(url="/simple", status_code=303)
    request.session["simple_prediction"] = {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "lower": result["lower"],
        "upper": result["upper"],
    }
    request.session["simple_form_data"] = form
    return RedirectResponse(url="/simple", status_code=303)

@app.get("/detail", response_class=HTMLResponse)
def detail_form(request: Request):
    ctx = {"groups": FEATURE_GROUPS}
    pred = request.session.pop("detail_prediction", None)
    err = request.session.pop("detail_error", None)
    form_data = request.session.pop("detail_form_data", None)
    if pred:
        ctx["prediction"] = pred["prediction"]
        ctx["confidence"] = pred["confidence"]
        ctx["lower"] = pred["lower"]
        ctx["upper"] = pred["upper"]
    if err:
        ctx["error"] = err
    if form_data:
        ctx["form_data"] = form_data
    else:
        ctx["form_data"] = {}
    return TEMPLATES.TemplateResponse(request, "detail.html", ctx)

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
        request.session["detail_error"] = f"Invalid input: {e.errors()[0]['msg']}"
        request.session["detail_form_data"] = form
        return RedirectResponse(url="/detail", status_code=303)
    df = pd.DataFrame([house.model_dump(by_alias=True)])
    try:
        result = model.predict_with_confidence(df)
    except Exception as e:
        logger.error(f"Detail prediction failed: {e}", exc_info=True)
        request.session["detail_error"] = "Prediction failed. Please check your inputs."
        request.session["detail_form_data"] = form
        return RedirectResponse(url="/detail", status_code=303)
    request.session["detail_prediction"] = {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "lower": result["lower"],
        "upper": result["upper"],
    }
    request.session["detail_form_data"] = form
    return RedirectResponse(url="/detail", status_code=303)

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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )