# src/data_generator.py

# Import necessary libraries
import pandas as pd  # For creating and manipulating dataframes
import numpy as np  # For numerical operations (not heavily used here)
from faker import Faker  # For generating realistic fake data
import random  # For random selections and numbers
from datetime import datetime, timedelta  # For handling dates and time
import os  # For file and directory operations

# Initialize Faker instance
fake = Faker()

# Ensure that the "data" directory exists, create if it doesn't
os.makedirs("data", exist_ok=True)


# Function to generate synthetic wallet/user data
def generate_wallet_data(n_wallets=100):
    """
    Generates a dataframe of wallet information.

    Parameters:
        n_wallets (int): Number of wallet records to generate.

    Returns:
        pd.DataFrame: Wallet data with columns - wallet_id, kyc_verified, registration_date
    """
    wallets = []
    for _ in range(n_wallets):
        wallets.append({
            "wallet_id": fake.uuid4(),  # Unique wallet ID using UUID
            "kyc_verified": random.choice([0, 1]),  # Randomly assign KYC verification (0 = No, 1 = Yes)
            "registration_date": fake.date_between(start_date='-2y', end_date='today')
            # Random registration in past 2 years
        })
    return pd.DataFrame(wallets)  # Convert list of dictionaries to a DataFrame


# Function to generate synthetic transaction data
def generate_transactions(wallets, n_transactions=1000):
    """
    Generates a dataframe of transactions linked to wallets.

    Parameters:
        wallets (pd.DataFrame): Wallet data to link transactions to.
        n_transactions (int): Number of transaction records to generate.

    Returns:
        pd.DataFrame: Transaction data with columns - transaction_id, wallet_id, timestamp, amount, type, ip_address
    """
    transactions = []
    for _ in range(n_transactions):
        # Randomly pick a wallet for this transaction
        wallet = wallets.sample(1).iloc[0]

        transactions.append({
            "transaction_id": fake.uuid4(),  # Unique transaction ID
            "wallet_id": wallet['wallet_id'],  # Link transaction to a wallet
            "timestamp": fake.date_time_between(start_date=wallet['registration_date'], end_date='now'),
            # Transaction date after wallet registration
            "amount": round(random.uniform(10, 5000), 2),  # Random transaction amount between 10 and 5000
            "type": random.choice(['deposit', 'transfer', 'redeem']),  # Random transaction type
            "ip_address": fake.ipv4(),  # Random IP address for transaction
        })
    return pd.DataFrame(transactions)  # Convert to DataFrame


# Main block: generate and save data
if __name__ == "__main__":
    # Generate wallet and transaction data
    wallets = generate_wallet_data(100)  # 100 wallets
    txns = generate_transactions(wallets, 1000)  # 1000 transactions linked to wallets

    # Save generated data as CSV files
    wallets.to_csv("data/wallets.csv", index=False)  # Wallet information
    txns.to_csv("data/generated_data.csv", index=False)  # Transaction records

    # Confirmation message
    print("Data generated successfully in 'data/' folder!")
