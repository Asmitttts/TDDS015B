from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
from pathlib import Path


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ChurnGuard AI API",
    description="API for predicting customer churn using Machine Learning",
    version="1.0.0"
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"

model = joblib.load(MODEL_PATH)


# ============================================================
# INPUT DATA MODEL
# ============================================================

class CustomerData(BaseModel):

    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)

    Partner: str
    Dependents: str

    tenure: int = Field(ge=0)

    PhoneService: str
    MultipleLines: str

    InternetService: str

    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str

    StreamingTV: str
    StreamingMovies: str

    Contract: str
    PaperlessBilling: str
    PaymentMethod: str

    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to ChurnGuard AI API",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict_churn(customer: CustomerData):

    # Convert incoming data into dictionary
    customer_data = customer.model_dump()

    # Create DataFrame with one customer
    import pandas as pd

    input_data = pd.DataFrame([customer_data])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get probability of churn
    probability = model.predict_proba(input_data)[0][1]

    # Convert probability into percentage
    churn_probability = round(probability * 100, 2)

    # Determine risk level
    if churn_probability < 30:
        risk_level = "Low"
    elif churn_probability < 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # Convert prediction to readable result
    churn_prediction = "Yes" if prediction == 1 else "No"

    # Generate recommendation
    if risk_level == "High":
        recommendation = (
            "High churn risk. Consider a retention offer, "
            "personalized support, or a long-term contract."
        )

    elif risk_level == "Medium":
        recommendation = (
            "Moderate churn risk. Consider improving customer "
            "engagement and service support."
        )

    else:
        recommendation = (
            "Low churn risk. Continue providing regular "
            "customer support and service."
        )

    return {
        "churn_prediction": churn_prediction,
        "churn_probability": churn_probability,
        "risk_level": risk_level,
        "recommendation": recommendation
    }