# src/feature_engineering.py

# Import pandas library for data manipulation
import pandas as pd


# Function to create features from transaction data
def create_features(transactions):
    """
    Generates new features for transactions to help in modeling.

    Parameters:
        transactions (pd.DataFrame): DataFrame containing transaction records.

    Returns:
        pd.DataFrame: DataFrame containing selected engineered features.
    """
    # Create a copy of the transactions dataframe to avoid modifying original data
    df = transactions.copy()

    # Extract the hour from the timestamp of the transaction
    # This feature captures the time of day when the transaction occurred
    df['hour'] = df['timestamp'].dt.hour

    # Create a binary feature indicating if the transaction amount is large
    # 1 if amount > 3000, else 0
    df['is_large_amount'] = (df['amount'] > 3000).astype(int)

    # Count the number of transactions per wallet
    # Here it counts all transactions per wallet (simplified, could be refined for last 1 hour)
    df['tx_count_1h'] = df.groupby('wallet_id')['transaction_id'].transform('count')

    # Return a dataframe containing only the engineered features
    return df[['amount', 'hour', 'is_large_amount', 'tx_count_1h']]


# Main execution block
if __name__ == "__main__":
    # Read the generated transaction data from CSV
    # Parse the 'timestamp' column as datetime objects for feature extraction
    txns = pd.read_csv("data/generated_data.csv", parse_dates=['timestamp'])

    # Generate features using the create_features function
    features = create_features(txns)

    # Save the engineered features to a new CSV file
    features.to_csv("data/features.csv", index=False)
