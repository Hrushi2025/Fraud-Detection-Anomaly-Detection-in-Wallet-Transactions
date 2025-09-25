# Fraud-Detection-Anomaly-Detection-in-Wallet-Transactions

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/547cf886-e894-466c-8166-defa8df6e490" />

Project Overview

**Objective:**  
Build a **real-time wallet activity monitoring system** to detect suspicious or fraudulent behavior using **unsupervised anomaly detection models**. The system identifies anomalies like:

- Rapid token transfers across wallets  
- High-volume or frequent redemptions  
- Login pattern anomalies  
- Suspicious crypto deposit behavior  

**Why this project matters:**  
Cryptocurrency and digital wallets are prone to fraud due to the lack of centralized control. Detecting anomalies early can prevent financial loss, ensure regulatory compliance, and maintain user trust.  

---

## Main Objectives

1. **Simulate wallet transactions and user login data** to create realistic testing scenarios.  
2. **Extract features** relevant to fraud detection, including:  
   - Transaction amount  
   - Transaction velocity (number of transactions in a time window)  
   - Geo/IP location changes  
   - KYC verification status  
3. **Train unsupervised anomaly detection models** (Isolation Forest / One-Class SVM) on these features.  
4. **Assign a fraud score** to each transaction or wallet.  
5. **Send alerts automatically** to an admin dashboard via API.  

---

## Tools & Libraries

| Category | Libraries / Tools | Purpose |
|----------|-----------------|--------|
| Programming | Python 3.10+ | Core programming language |
| Data Manipulation & Analysis | pandas, numpy, datetime | Load, clean, and transform transaction data |
| Machine Learning / Anomaly Detection | scikit-learn (IsolationForest, OneClassSVM), pyod (optional) | Train models to detect anomalies |
| Visualization | matplotlib, seaborn | Plot data distributions and anomalies |
| APIs / Real-Time Simulation | FastAPI, uvicorn, requests | Serve alert API and simulate alert sending |
| Optional / Enhancement | Faker, GeoIP2, ip2geotools | Generate synthetic users, transactions, and simulate location features |

---

## Project Structure


<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/dd0b037c-3000-4bff-a09e-50eb0198db7c" />



Step-by-Step Approach

### Step 1: Generate Synthetic Wallet Data
- Simulate **users**: wallet ID, KYC status, registration date  
- Simulate **transactions**: transaction ID, wallet ID, timestamp, amount, type (deposit, transfer, redeem), IP/geo location  

> The synthetic dataset allows testing the anomaly detection system in a controlled environment.

---

### Step 2: Feature Engineering
- Compute meaningful features for each transaction or wallet:  
  - Transaction amount  
  - Number of transactions in the last X minutes/hours (velocity)  
  - Average transaction amount per wallet  
  - Geo/IP anomaly detection (e.g., sudden country or IP change)  
  - KYC verification status  

> Features are critical for the anomaly detection model to correctly flag suspicious behavior.

---

### Step 3: Train Anomaly Detection Model
- Use **Isolation Forest** or **One-Class SVM** to train on numeric features extracted from transactions.  
- Save the trained model as `models/fraud_model.pkl` for later use.  
- The model identifies unusual patterns without needing labeled fraud data (unsupervised).

---

### Step 4: Detect Anomalies
- Load new transactions and extract features.  
- Use the trained model to generate:  
  - **Fraud score** for each transaction  
  - **Anomaly flag** (`True` / `False`)  
- Transactions with `is_anomaly=True` are considered suspicious.

---

### Step 5: Alert System
- **FastAPI server (`alert_api.py`)** receives alerts via `/alert` endpoint.  
- For every anomaly, an alert is printed or can be logged to a database / sent to an admin dashboard.  
- Example alert:   Alerts can also trigger emails, SMS, or notifications depending on implementation.

## How the Scripts Work Together

1. **`data_generator.py`** → Generates synthetic wallet and transaction data.  
2. **`feature_engineering.py`** → Converts raw data into features for modeling.  
3. **`train_model.py`** → Trains anomaly detection model and saves it.  
4. **`detect_anomalies.py`** → Loads new transactions, detects anomalies, and sends alerts via API.  
5. **`alert_api.py`** → Receives alerts and prints/logs them for admins.  
6. **Optional**: `notebooks/eda_and_modeling.ipynb` for analysis and visualization.

## Key Features of the System

- **Unsupervised anomaly detection** – doesn’t need labeled fraud data.  
- **Real-time alerts** – detects suspicious activity and notifies admin immediately.  
- **Scalable and modular** – components (data generation, feature extraction, model, API) are decoupled.  
- **Customizable features** – can add new fraud indicators like velocity, geo/IP anomalies, KYC flags.

  

