import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
import mlflow
import mlflow.sklearn
import joblib
from pathlib import Path

# Set MLflow tracking URI to local directory
mlflow.set_tracking_uri("file:./mlruns")

# Create experiment
experiment_name = "shieldops-resolution-hours"
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(experiment_name)
else:
    experiment_id = experiment.experiment_id

# Load data
df = pd.read_csv("data/training_data.csv")
X = df[["severity_level", "alerts_count", "analyst_experience", "is_automated"]]
y = df["resolution_hours"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Track models and results
results = {
    "experiment_name": experiment_name,
    "models": [],
    "best_model": "",
    "best_metric_name": "rmse",
    "best_metric_value": 0.0
}

# Train LinearRegression
with mlflow.start_run(experiment_id=experiment_id):
    mlflow.set_tag("domain", "secops___cybersecurity")
    
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    
    y_pred = model_lr.predict(X_test)
    mae_lr = mean_absolute_error(y_test, y_pred)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred))
    
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("MAE", mae_lr)
    mlflow.log_metric("RMSE", rmse_lr)
    
    run_id_lr = mlflow.active_run().info.run_id
    
    results["models"].append({
        "name": "LinearRegression",
        "mae": float(mae_lr),
        "rmse": float(rmse_lr)
    })
    
    print(f"LinearRegression - MAE: {mae_lr:.4f}, RMSE: {rmse_lr:.4f}")

# Train Ridge
with mlflow.start_run(experiment_id=experiment_id):
    mlflow.set_tag("domain", "secops___cybersecurity")
    
    model_ridge = Ridge(alpha=1.0)
    model_ridge.fit(X_train, y_train)
    
    y_pred = model_ridge.predict(X_test)
    mae_ridge = mean_absolute_error(y_test, y_pred)
    rmse_ridge = np.sqrt(mean_squared_error(y_test, y_pred))
    
    mlflow.log_param("model_type", "Ridge")
    mlflow.log_param("alpha", 1.0)
    mlflow.log_metric("MAE", mae_ridge)
    mlflow.log_metric("RMSE", rmse_ridge)
    
    run_id_ridge = mlflow.active_run().info.run_id
    
    results["models"].append({
        "name": "Ridge",
        "mae": float(mae_ridge),
        "rmse": float(rmse_ridge)
    })
    
    print(f"Ridge - MAE: {mae_ridge:.4f}, RMSE: {rmse_ridge:.4f}")

# Select best model by RMSE
if rmse_lr < rmse_ridge:
    best_model = model_lr
    best_type = "LinearRegression"
    best_rmse = rmse_lr
    best_mae = mae_lr
else:
    best_model = model_ridge
    best_type = "Ridge"
    best_rmse = rmse_ridge
    best_mae = mae_ridge

# Save best model
Path("models").mkdir(exist_ok=True)
model_path = f"models/best_model_{best_type}.pkl"
joblib.dump(best_model, model_path)

results["best_model"] = best_type
results["best_metric_value"] = float(best_rmse)

# Save results
Path("results").mkdir(exist_ok=True)
with open("results/step1_s1.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "="*50)
print(f"✓ Best model: {best_type}")
print(f"✓ RMSE: {best_rmse:.4f}")
print(f"✓ Model saved to: {model_path}")
print(f"✓ Results saved to: results/step1_s1.json")
print("="*50)
