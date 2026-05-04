# MLOps Lab Complete - Deployment Guide

## Project Summary
This is a complete end-to-end MLOps lab implementing security incident resolution time prediction with experiment tracking, CLI, API, and monitoring.

---

## FOLDER STRUCTURE

```
Internals_Basics/
└── MLOPs_Lab_CIE/
    ├── data/
    │   ├── training_data.csv          # 30 training samples
    │   └── new_data.csv               # 8 test samples
    ├── src/
    │   ├── __init__.py                # Package init
    │   ├── train.py                   # Model training with MLflow
    │   ├── predict_cli.py             # CLI prediction tool
    │   ├── api.py                     # FastAPI application
    │   ├── simulate_traffic.py        # Traffic simulation
    │   └── monitor.py                 # Data drift monitoring
    ├── models/
    │   └── best_model_LinearRegression.pkl  # Trained model
    ├── logs/
    │   └── predictions.jsonl          # API prediction logs
    ├── results/
    │   ├── step1_s1.json              # Training results
    │   ├── step2_s3.json              # CLI prediction output
    │   ├── step3_s4.json              # API prediction output
    │   └── step4_s5.json              # Monitoring results
    ├── main.py                        # FastAPI entry point
    ├── generate_outputs.py            # Output generator
    ├── requirements.txt               # Python dependencies
    ├── Dockerfile                     # Docker configuration
    ├── .gitignore                     # Git ignore rules
    └── README.md                      # This file
```

---

## STEP-BY-STEP TERMINAL COMMANDS

### 1. Clone and Setup Repository

```powershell
# Navigate to workspace
cd c:\Users\aayus\Downloads\MLOPS\Internals_Basics\MLOPs_Lab_CIE

# Initialize Git (already done)
git init

# Add all files (already done)
git add .

# Commit (already done)
git commit -m "MLOps CIE complete"
```

### 2. To Push to GitHub (First Time Setup)

```powershell
# Create a new repository on GitHub called "Internals_Basics"
# Make it PUBLIC

# Then run:
git remote add origin https://github.com/YOUR_USERNAME/Internals_Basics.git
git branch -M main
git push -u origin main
```

### 3. Setup Python Environment

```powershell
cd c:\Users\aayus\Downloads\MLOPS\Internals_Basics\MLOPs_Lab_CIE

# Install requirements
pip install -r requirements.txt
```

### 4. Run Training with MLflow

```powershell
python src/train.py

# Output:
# ✓ LinearRegression - MAE: 0.1833, RMSE: 0.2017
# ✓ Ridge - MAE: 0.2137, RMSE: 0.2314
# ✓ Best model: LinearRegression
# ✓ Results saved to: results/step1_s1.json
```

### 5. Test CLI Prediction

```powershell
python src/predict_cli.py --severity_level 2 --alerts_count 18 --analyst_experience 10 --is_automated 0

# Output: JSON with prediction
```

### 6. Start FastAPI Server (Terminal 1)

```powershell
python main.py

# Output:
# Model loaded: models\best_model_LinearRegression.pkl
# INFO:     Uvicorn running on http://0.0.0.0:9000
```

### 7. Simulate Traffic (Terminal 2)

```powershell
python src/simulate_traffic.py

# Output:
# Sending 50 total requests:
#   - 40 normal requests
#   - 10 drifted requests
# Simulation complete! Successful: 50/50
```

### 8. Run Monitoring Analysis

```powershell
python src/monitor.py

# Output:
# ✓ Monitoring results saved to: results/step4_s5.json
# ⚠️  DATA DRIFT DETECTED: SEVERITY_DRIFT
```

### 9. Build Docker Image

```powershell
docker build -t shieldops-predictor:v1 .
```

### 10. Run Docker Container

```powershell
docker run shieldops-predictor:v1 --severity_level 2 --alerts_count 18 --analyst_experience 10 --is_automated 0

# Output: Prediction JSON
```

---

## EXPECTED JSON OUTPUTS

### results/step1_s1.json (Training Results)
```json
{
  "models_trained": [
    {
      "model_type": "LinearRegression",
      "MAE": 0.1833,
      "RMSE": 0.2017,
      "run_id": "..."
    },
    {
      "model_type": "Ridge",
      "alpha": 1.0,
      "MAE": 0.2137,
      "RMSE": 0.2314,
      "run_id": "..."
    }
  ],
  "best_model": {
    "model_type": "LinearRegression",
    "model_path": "models/best_model_LinearRegression.pkl",
    "MAE": 0.1833,
    "RMSE": 0.2017
  },
  "metrics": {
    "training_data_mean_severity": 2.75,
    "training_data_mean_alerts": 31.08,
    "training_data_mean_experience": 9.92,
    "test_size": 0.2,
    "random_state": 42
  }
}
```

### results/step2_s3.json (CLI Prediction)
```json
{
  "input": {
    "severity_level": 2,
    "alerts_count": 18,
    "analyst_experience": 10,
    "is_automated": 0
  },
  "prediction": 2.4897,
  "model_path": "models\\best_model_LinearRegression.pkl"
}
```

### results/step3_s4.json (API Prediction)
```json
{
  "input": {
    "severity_level": 2,
    "alerts_count": 18,
    "analyst_experience": 10,
    "is_automated": 0
  },
  "prediction": 2.4897,
  "model": "models/best_model_LinearRegression.pkl",
  "version": "1.0"
}
```

### results/step4_s5.json (Monitoring)
```json
{
  "total_predictions": 50,
  "statistics": {
    "mean_severity_level": 4.54,
    "mean_alerts_count": 37.70,
    "mean_analyst_experience": 9.98,
    "mean_is_automated": 0.42
  },
  "drift_detection": {
    "severity_threshold": 0.88,
    "alerts_threshold": 12.71,
    "alerts": [
      {
        "type": "SEVERITY_DRIFT",
        "current_mean": 4.54,
        "threshold": 0.88,
        "diff": 1.74,
        "status": "ALERT"
      }
    ],
    "drift_detected": true
  }
}
```

---

## API ENDPOINTS

### 1. Health Check
```bash
curl http://localhost:9000/ping

# Response:
{
  "status": "running",
  "model": "models/best_model_LinearRegression.pkl",
  "version": "1.0"
}
```

### 2. Make Prediction
```bash
curl -X POST http://localhost:9000/infer \
  -H "Content-Type: application/json" \
  -d '{
    "severity_level": 2,
    "alerts_count": 18,
    "analyst_experience": 10,
    "is_automated": 0
  }'

# Response:
{
  "input": {
    "severity_level": 2,
    "alerts_count": 18,
    "analyst_experience": 10,
    "is_automated": 0
  },
  "prediction": 2.4897,
  "model": "models/best_model_LinearRegression.pkl",
  "version": "1.0"
}
```

---

## DOCKER COMMANDS

### Build Image
```bash
docker build -t shieldops-predictor:v1 .
```

### Run Container (Interactive)
```bash
docker run -p 9000:9000 shieldops-predictor:v1
```

### Run Container (CLI Mode)
```bash
docker run shieldops-predictor:v1 --severity_level 2 --alerts_count 18 --analyst_experience 10 --is_automated 0
```

### Check Container Health
```bash
docker ps
docker logs <CONTAINER_ID>
```

---

## MLFLOW COMMANDS

### View Experiments
```bash
mlflow ui
# Access at: http://localhost:5000
```

### Check Tracking Directory
```bash
# Logs stored in:
# ./mlruns/
```

### View Specific Run
```bash
mlflow runs show <RUN_ID>
```

---

## GIT COMMANDS

### Configure User (Already Done)
```bash
git config user.email "aayushprof7633@gmail.com"
git config user.name "MLOps Engineer"
```

### Check Status
```bash
git status
git log
```

### Push to GitHub
```bash
# Create repo on GitHub: Internals_Basics (PUBLIC)
git remote add origin https://github.com/YOUR_USERNAME/Internals_Basics.git
git branch -M main
git push -u origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

---

## KEY PARAMETERS USED

| Parameter | Value | Purpose |
|-----------|-------|---------|
| test_size | 0.2 | 20% data for testing |
| random_state | 42 | Reproducibility |
| Ridge alpha | 1.0 | Regularization strength |
| Severity threshold | 0.88 | Drift detection tolerance |
| Alerts threshold | 12.71 | Drift detection tolerance |
| Port | 9000 | FastAPI server port |
| Traffic | 50 requests | 40 normal + 10 drifted |

---

## MODEL PERFORMANCE

- **Best Model**: LinearRegression
- **MAE (Mean Absolute Error)**: 0.1833 hours
- **RMSE (Root Mean Squared Error)**: 0.2017 hours
- **Training/Test Split**: 24 samples / 6 samples
- **Features**: 4 (severity_level, alerts_count, analyst_experience, is_automated)
- **Target**: resolution_hours

---

## MONITORING RESULTS

- **Total Predictions**: 50 (40 normal + 10 drifted)
- **Data Drift Detected**: YES (Severity increased from 2.75 to 4.54)
- **Severity Drift**: ALERT (difference: 1.74 > threshold: 0.88)
- **Alerts Drift**: No alert (within threshold)

---

## PRODUCTION CHECKLIST

✅ Data preparation and validation
✅ Model training with experiment tracking
✅ Model versioning (LinearRegression selected)
✅ CLI interface for batch predictions
✅ REST API for real-time predictions
✅ Pydantic validation for inputs
✅ Request/response logging
✅ Data drift monitoring
✅ Docker containerization
✅ Requirements management
✅ Version control (Git)
✅ All outputs in JSON format

---

## TROUBLESHOOTING

### API won't start
```powershell
# Check if port 9000 is in use
netstat -ano | findstr :9000

# Kill process if needed
taskkill /PID <PID> /F
```

### Model not found
```powershell
# Ensure train.py was run first
python src/train.py
```

### Docker build fails
```powershell
# Rebuild without cache
docker build --no-cache -t shieldops-predictor:v1 .
```

### Git push fails
```powershell
# Check remote
git remote -v

# Remove wrong remote if needed
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/Internals_Basics.git
```

---

## RESOURCES

- **MLflow Docs**: https://mlflow.org/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Scikit-learn**: https://scikit-learn.org/
- **Docker Docs**: https://docs.docker.com/
- **Git Docs**: https://git-scm.com/doc/

---

**Lab Created**: May 4, 2026
**Status**: ✅ COMPLETE - Ready for Production Deployment
