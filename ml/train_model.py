import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

file_path = "data/Telco-Customer-Churn.csv"
df = pd.read_csv(file_path)

print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")


# ============================================================
# 2. CLEAN DATA
# ============================================================

print("\nCleaning data...")

# TotalCharges contains some blank values.
# Convert it from text to numeric.
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove customerID because it is only an identifier
# and does not provide useful predictive information.
df = df.drop(columns=["customerID"])

# Convert target column:
# No  -> 0
# Yes -> 1
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

print("Data cleaning completed.")


# ============================================================
# 3. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

print(f"\nNumber of features: {X.shape[1]}")
print(f"Target variable: Churn")


# ============================================================
# 4. IDENTIFY COLUMN TYPES
# ============================================================

numeric_features = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

categorical_features = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod"
]


# ============================================================
# 5. CREATE PREPROCESSING PIPELINE
# ============================================================

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)


categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_transformer,
            numeric_features
        ),
        (
            "categorical",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ============================================================
# 6. SPLIT DATA INTO TRAINING AND TESTING
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nData split completed.")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ============================================================
# 7. DEFINE MACHINE LEARNING MODELS
# ============================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}


# ============================================================
# 8. TRAIN AND EVALUATE MODELS
# ============================================================

results = {}
trained_pipelines = {}

print("\n" + "=" * 60)
print("MODEL TRAINING AND EVALUATION")
print("=" * 60)


for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # Train model
    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Probability of churn
    y_probability = pipeline.predict_proba(X_test)[:, 1]

    # Evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_probability)

    results[model_name] = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4)
    }

    trained_pipelines[model_name] = pipeline

    print(f"\n{model_name}")
    print("-" * 40)
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")


# ============================================================
# 9. SELECT BEST MODEL
# ============================================================

best_model_name = max(
    results,
    key=lambda model: results[model]["roc_auc"]
)

best_pipeline = trained_pipelines[best_model_name]

print("\n" + "=" * 60)
print("BEST MODEL")
print("=" * 60)

print(f"Selected model: {best_model_name}")
print(f"ROC-AUC: {results[best_model_name]['roc_auc']}")


# ============================================================
# 10. SAVE BEST MODEL
# ============================================================

model_path = "models/churn_model.pkl"

joblib.dump(best_pipeline, model_path)

print(f"\nModel saved successfully to: {model_path}")


# ============================================================
# 11. SAVE MODEL RESULTS
# ============================================================

results_path = "models/model_results.json"

with open(results_path, "w") as file:
    json.dump(
        {
            "best_model": best_model_name,
            "results": results
        },
        file,
        indent=4
    )

print(f"Model evaluation results saved to: {results_path}")


print("\nTraining completed successfully! 🎉")