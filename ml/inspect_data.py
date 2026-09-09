import pandas as pd

# Load the dataset
file_path = "data/Telco-Customer-Churn.csv"
df = pd.read_csv(file_path)

# Basic information
print("\n========== DATASET SHAPE ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Column names
print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print(column)

# Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# First 5 records
print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

# Churn distribution
print("\n========== CHURN DISTRIBUTION ==========")
print(df["Churn"].value_counts())

print("\n========== CHURN PERCENTAGE ==========")
print(df["Churn"].value_counts(normalize=True) * 100)