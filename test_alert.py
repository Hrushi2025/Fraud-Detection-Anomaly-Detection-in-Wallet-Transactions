# Import the requests library to make HTTP requests
import requests

# Define the alert payload as a Python dictionary
# This payload contains information about a suspicious transaction
alert = {
    "wallet_id": "1234-abcd",         # Unique identifier of the wallet
    "transaction_id": "tx-5678",      # Unique identifier of the transaction
    "fraud_score": -0.25               # Fraud score indicating likelihood of fraud (negative/positive values based on model)
}

# Send a POST request to the FastAPI alert endpoint
# The 'json=alert' parameter automatically converts the Python dictionary to JSON format
response = requests.post("http://127.0.0.1:8000/alert", json=alert)

# Print the JSON response returned by the API
# This will confirm whether the alert was successfully received
print(response.json())

