from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI()

class ScoringItem(BaseModel): 
    YearsAtCompany: float
    EmployeeSatisfaction: float
    Position: str
    Salary: int

model_path = "rfmodel.pkl"
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {model_path}: {e}")

@app.get("/ping")
def ping():
    return {"message": "API is live!"}

@app.post("/")
async def scoring_endpoint(item: ScoringItem): 
    input_df = pd.DataFrame([item.dict()])
    prediction = model.predict(input_df)
    return {"prediction": int(prediction[0])}
