from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import logging

from redis import asyncio

from typing import Any
import numpy as np
import joblib
from datetime import datetime
import os

app = FastAPI()
model = joblib.load("./src/model_pipeline.pkl")

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"

@app.on_event("startup")
def startup():
    HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.debug(HOST_URL)
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

class House(BaseModel):
    MedInc: float
    HouseAge: int
    AveRooms: float
    AveBedrms: float
    Population: int | None = None
    AveOccup: float | None = None
    Latitude: float
    Longitude: float
    
    def to_np(self):
        return np.array(list(vars(self).values())).reshape(1, 8)
    
    #Latitude is specified in degrees within the range [-90, 90]
    @validator('Latitude')
    def lat_must_be_in_range(cls, v):
        if v <  -90 or v > 90:
            raise ValueError('not a valid latitude')
        return v
    
    #Longitude is specified in degrees within the range [-180, 180]
    @validator('Longitude')
    def long_must_be_in_range(cls, v):
        if v <  -180 or v > 180:
            raise ValueError('not a valid longitude')
        return v

class HouseList(BaseModel):
    houses: list[House]

    def to_np(self):
        return np.vstack([x.to_np() for x in self.houses])

class Prediction(BaseModel):
    prediction: list[float]

# class PredictionList(BaseModel):
#     list = list[Prediction]

@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="not implemented")  # endpoint not found


@app.get("/hello")
# @cache(expire=60)
async def hello_user(name: str = ""):
    if name == "":
        raise HTTPException(
            status_code=422,  # 422 status The request was well-formed but was unable to be followed due to semantic errors.
            detail="Please provide a valid 'name' query parameter",
        )
    greeting = str("hello " + name)
    return greeting

@app.post("/predict", response_model=Prediction)
@cache(expire=60)
async def predict_home_price(houses:HouseList):
    predictions = model.predict(houses.to_np())
    return {"predictions": list(predictions)}

@app.get("/health")
async def health():
    return datetime.now().isoformat()

