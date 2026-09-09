# 🛡️ ChurnGuard AI

## AI-Powered Customer Churn Prediction System

ChurnGuard AI is a machine-learning-based customer churn prediction system that predicts whether a customer is likely to leave a service.

The project combines Machine Learning, FastAPI, and Streamlit to provide an interactive system where users can enter customer information and receive a churn prediction, probability score, risk level, and recommended action.

---

## 🎯 Problem Statement

Customer churn is a major challenge for service-based companies. Losing customers can reduce revenue and increase the cost of acquiring new customers.

ChurnGuard AI uses customer information such as tenure, services, contract type, payment method, and monthly charges to identify customers who may be at risk of leaving.

---

## 🎯 Objectives

- Predict whether a customer is likely to churn.
- Calculate the probability of customer churn.
- Classify customers into Low, Medium, or High risk.
- Provide recommended actions for customer retention.
- Provide an API for machine-learning predictions.
- Create an easy-to-use web interface for users.

---

## 🧠 Machine Learning

The system uses the Telco Customer Churn dataset containing customer demographic, service, and billing information.

The trained model is stored in:

`models/churn_model.pkl`

Model results are stored in:

`models/model_results.json`

The model takes customer information as input and produces a churn prediction and probability.

---

## 🏗️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Uvicorn
- Streamlit
- Joblib
- JSON
- Machine Learning

---

## 📁 Project Structure

```text
ChurnGuard-AI/
│
├── backend/
│   └── main.py
│
├── data/
│   └── Telco-Customer-Churn.csv
│
├── frontend/
│   ├── app.py
│   └── app_backup.py
│
├── ml/
│   ├── inspect_data.py
│   └── train_model.py
│
├── models/
│   ├── churn_model.pkl
│   └── model_results.json
│
├── README.md
└── requirements.txt