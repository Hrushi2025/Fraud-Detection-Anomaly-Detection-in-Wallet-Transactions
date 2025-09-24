# src/detect_anomalies.py

# Import pandas for data manipulation
import pandas as pd

# Import joblib to load the trained scikit-learn model
import joblib

# Import requests to send HTTP requests to the alert API
import requests

# Import the create_features function from feature_engineering.py
# This will be used to generate model input features from raw transactions
from feature_engineering import create_features

# Load the pre-trained Isolation Forest model for anomaly detection
# This model was trained in train_model.py
model = joblib.load("models/fraud_model.pkl")

# Define the URL of the FastAPI alert server
# This is where alerts for suspicious transactions will be sent
ALERT_API_URL = "http://127.0.0.1:8000/alert"


# Function to detect anomalies in new transactions
def detect_anomalies(new_transactions):
    """
    Detects anomalies in a given set of transactions using the trained model.

    Parameters:
        new_transactions (pd.DataFrame): Raw transaction data.

    Returns:
        pd.DataFrame: Original transactions with additional columns:
            - fraud_score: model's anomaly score
            - is_anomaly: True if transaction is considered anomalous
    """
    # Generate features from the raw transactions
    features = create_features(new_transactions)

    # Compute anomaly scores using the Isolation Forest model
    # Higher (more positive) scores indicate normal, lower (negative) scores indicate anomalies
    new_transactions['fraud_score'] = model.decision_function(features)

    # Predict anomalies: -1 indicates anomaly, 1 indicates normal
    new_transactions['is_anomaly'] = model.predict(features) == -1

    # Return the original dataframe with fraud_score and is_anomaly columns added
    return new_transactions


# Function to send anomaly alerts to the FastAPI server
def send_alerts(anomalies_df):
    """
    Sends each detected anomaly to the alert API.

    Parameters:
        anomalies_df (pd.DataFrame): DataFrame containing detected anomalies
    """
    # Iterate over each row in the anomalies dataframe
    for _, row in anomalies_df.iterrows():
        # Prepare the alert payload
        alert = {
            "wallet_id": row['wallet_id'],  # Wallet ID of the suspicious transaction
            "transaction_id": row['transaction_id'],  # Transaction ID
            "fraud_score": row['fraud_score']  # Anomaly score from the model
        }
        try:
            # Send a POST request to the alert API with the payload as JSON
            response = requests.post(ALERT_API_URL, json=alert)

            # Check if the request was successful
            if response.status_code == 200:
                print(f"Alert sent for transaction {row['transaction_id']}")
            else:
                # Handle failure response from the API
                print(f"Failed to send alert for {row['transaction_id']}: {response.text}")
        except Exception as e:
            # Handle exceptions such as network errors
            print(f"Error sending alert for {row['transaction_id']}: {e}")


# Main execution block
if __name__ == "__main__":
    # Load new transactions from CSV
    # 'timestamp' column is parsed as datetime for feature creation
    new_txns = pd.read_csv("data/generated_data.csv", parse_dates=['timestamp'])

    # Detect anomalies in the loaded transactions
    result = detect_anomalies(new_txns)

    # Filter only the transactions flagged as anomalies
    anomalies = result[result['is_anomaly'] == True]

    # Check if any anomalies were detected
    if anomalies.empty:
        print("No anomalies detected.")
    else:
        print("Detected anomalies:")
        print(anomalies)

        # Send alerts for each detected anomaly to the FastAPI server
        send_alerts(anomalies)
