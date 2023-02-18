from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, validator, parse_obj_as
import numpy as np
import joblib
from datetime import datetime
from typing import List

app = FastAPI()
model = joblib.load("./trainer/model_pipeline.pkl")

class House(BaseModel):
    MedInc: float
    HouseAge: int
    AveRooms: float
    AveBedrms: float
    Population: int | None = None
    AveOccup: float | None = None
    Latitude: float
    Longitude: float
    
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

@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="not implemented")  # endpoint not found


@app.get("/hello")
async def hello_user(name: str = ""):
    if name == "":
        raise HTTPException(
            status_code=422,  # 422 status The request was well-formed but was unable to be followed due to semantic errors.
            detail="Please provide a valid 'name' query parameter",
        )
    greeting = str("hello " + name)
    return greeting

@app.post("/predict")
async def predict_home_price(home:List[House]):
    homes = np.array(home)
    features = [dict(x) for x in homes]
    return [model.predict([[feature[key] for key in feature.keys()]])[0]
                   for feature in features]

@app.get("/health")
async def health():
    return datetime.now().isoformat()
