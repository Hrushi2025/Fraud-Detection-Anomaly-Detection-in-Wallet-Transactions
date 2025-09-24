# src/train_model.py

# Import pandas for reading feature CSVs
import pandas as pd

# Import IsolationForest from scikit-learn for anomaly detection
from sklearn.ensemble import IsolationForest

# Import joblib for saving the trained model to disk
import joblib

# Import os for directory operations
import os

# Ensure that the "models" directory exists; create it if it doesn't
os.makedirs("models", exist_ok=True)

# Load the engineered features from the CSV file
# These features were generated in feature_engineering.py
features = pd.read_csv("data/features.csv")

# Initialize the Isolation Forest model
# n_estimators=100 -> number of trees in the forest
# contamination=0.05 -> assume ~5% of transactions are anomalies
# random_state=42 -> ensures reproducible results
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

# Fit the model on the feature data
# The model learns patterns of normal vs anomalous transactions
model.fit(features)

# Save the trained model to the "models" folder as 'fraud_model.pkl'
# joblib is used because it efficiently serializes large scikit-learn models
joblib.dump(model, "models/fraud_model.pkl")

# Print confirmation that the model has been trained and saved
print("Model trained and saved in 'models/' folder!")
