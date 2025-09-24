# api/alert_api.py

# Import FastAPI to create the API application
from fastapi import FastAPI

# Import BaseModel from Pydantic for request validation
from pydantic import BaseModel

# Import uvicorn to run the FastAPI server
import uvicorn

# Initialize the FastAPI app
app = FastAPI()


# Define the data model for incoming alert requests
class Alert(BaseModel):
    """
    Pydantic model defining the structure of an alert request.

    Attributes:
        wallet_id (str): Unique identifier of the wallet
        transaction_id (str): Unique identifier of the transaction
        fraud_score (float): The score indicating likelihood of fraud
    """
    wallet_id: str
    transaction_id: str
    fraud_score: float


# Define a POST endpoint to receive alerts
@app.post("/alert")
def send_alert(alert: Alert):
    """
    Endpoint to handle incoming alerts about suspicious transactions.

    Parameters:
        alert (Alert): The alert payload containing wallet_id, transaction_id, and fraud_score.

    Actions:
        - Prints the alert message to console
        - Can be extended to send email, log to database, or notify admin
    """
    # Print alert details to the console for monitoring/logging
    print(
        f"ALERT: Wallet {alert.wallet_id} has suspicious transaction {alert.transaction_id} with score {alert.fraud_score}")

    # Return a JSON response confirming the alert has been sent
    return {"status": "alert sent"}


# Run the FastAPI server if this script is executed directly
if __name__ == "__main__":
    # Start the uvicorn server on all interfaces at port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
