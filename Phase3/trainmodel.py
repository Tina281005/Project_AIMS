import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 1. Load your data
df = pd.read_csv("../server_metrics_week.csv")

# 2. Convert timestamp to datetime and add time-based features
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["dayofweek"] = df["timestamp"].dt.dayofweek

# 3. Sort data for each server to align predictions
df = df.sort_values(by=["server_name", "timestamp"])

# 4. Choose your prediction target: next time-step's CPU load
df["cpu_load_next"] = df.groupby("server_name")["cpu_load_percent"].shift(-1)

# Remove last record for each server (because we can't predict "next" for it)
df = df.dropna(subset=["cpu_load_next"])

# Convert server_name to a numerical format using one-hot encoding
df = pd.get_dummies(df, columns=['server_name'], prefix='server')

# 5. Define features and target
feature_cols = [
    "latency_ms",
    "cpu_load_percent",
    "packet_loss_percent",
    "jitter_ms",
    "active_requests",
    "hour",
    "dayofweek",
    # Add the new server columns to the features
    'server_Server1', 
    'server_Server2', 
    'server_Server3', 
    'server_Server4' 
]
X = df[feature_cols]
y = df["cpu_load_next"]

# 6. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Train your model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluate model
y_pred = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# 9. Save model for later use
joblib.dump(model, "cpu_load_predictor_rf.joblib")
print("Trained model saved as cpu_load_predictor_rf.joblib")
