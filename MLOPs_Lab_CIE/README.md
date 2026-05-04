# MLOPs_Lab_CIE - Security Incident Resolution Prediction

A production-grade MLOps implementation featuring experiment tracking, REST API, CLI tools, Docker containerization, and real-time monitoring for predicting security incident resolution times.

## 🎯 Project Overview

This lab demonstrates a complete MLOps pipeline for a cybersecurity use case:
- **Goal**: Predict the time needed to resolve security incidents
- **Model**: LinearRegression (selected over Ridge based on RMSE)
- **Features**: 4 input parameters (severity, alerts count, analyst experience, automation status)
- **Output**: Resolution time in hours

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Internals_Basics.git
cd Internals_Basics/MLOPs_Lab_CIE

# Install dependencies
pip install -r requirements.txt

# Train model
python src/train.py

# Start API server
python main.py

# In another terminal, run traffic simulation
python src/simulate_traffic.py

# Monitor results
python src/monitor.py
```

## 📁 Project Structure

- **data/**: Training and test datasets
- **src/**: Source code modules
- **models/**: Trained model artifacts
- **logs/**: API prediction logs (JSONL format)
- **results/**: Step-wise JSON outputs
- **Dockerfile**: Container configuration
- **requirements.txt**: Python dependencies

## 🚀 Features

### 1. Experiment Tracking (MLflow)
```bash
python src/train.py
```
- Trains LinearRegression and Ridge models
- Logs parameters (model type, alpha)
- Logs metrics (MAE, RMSE)
- Automatically selects best model by RMSE

### 2. Command-Line Interface
```bash
python src/predict_cli.py --severity_level 2 --alerts_count 18 --analyst_experience 10 --is_automated 0
```
- Batch predictions
- JSON output
- Load and inference capabilities

### 3. REST API (FastAPI)
```bash
python main.py
```
- **GET /ping** - Health check
- **POST /infer** - Make predictions
- Automatic request/response logging
- Pydantic input validation
- Runs on port 9000

### 4. Traffic Simulation
```bash
python src/simulate_traffic.py
```
- Generates 50 requests (40 normal + 10 anomalies)
- Tests API robustness
- Creates prediction logs

### 5. Monitoring & Drift Detection
```bash
python src/monitor.py
```
- Analyzes prediction statistics
- Detects data drift
- Generates monitoring reports

## 🐳 Docker

```bash
# Build image
docker build -t shieldops-predictor:v1 .

# Run container
docker run shieldops-predictor:v1 --severity_level 2 --alerts_count 18 --analyst_experience 10 --is_automated 0

# Run API
docker run -p 9000:9000 shieldops-predictor:v1
```

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Model | LinearRegression |
| MAE | 0.1833 hours |
| RMSE | 0.2017 hours |
| Test Set Size | 6 samples |
| Training Samples | 24 |

## 📋 API Examples

### Health Check
```bash
curl http://localhost:9000/ping
```

### Make Prediction
```bash
curl -X POST http://localhost:9000/infer \
  -H "Content-Type: application/json" \
  -d '{
    "severity_level": 2,
    "alerts_count": 18,
    "analyst_experience": 10,
    "is_automated": 0
  }'
```

## 📈 Monitoring Output

```json
{
  "total_predictions": 50,
  "statistics": {
    "mean_severity_level": 4.54,
    "mean_alerts_count": 37.70
  },
  "drift_detection": {
    "drift_detected": true,
    "alerts": [...]
  }
}
```

## 🔧 Configuration

- **Test Size**: 0.2 (20%)
- **Random State**: 42 (reproducibility)
- **API Port**: 9000
- **Log Format**: JSONL

## 📦 Dependencies

```
pandas==2.0.3
scikit-learn==1.3.0
mlflow==2.4.1
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
joblib==1.3.2
```

## 📝 Output Files

- **results/step1_s1.json** - Training metrics
- **results/step2_s3.json** - CLI prediction
- **results/step3_s4.json** - API prediction
- **results/step4_s5.json** - Monitoring results
- **logs/predictions.jsonl** - API request logs

## 🎓 Learning Outcomes

This lab covers:
- ✅ Experiment tracking with MLflow
- ✅ REST API development with FastAPI
- ✅ Command-line tool creation
- ✅ Data validation with Pydantic
- ✅ Docker containerization
- ✅ Monitoring and drift detection
- ✅ Version control with Git

## 🔗 Links

- [MLflow Documentation](https://mlflow.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Docker Documentation](https://docs.docker.com/)

## 📄 License

MIT

## 👤 Author

MLOps Engineer
aayushprof7633@gmail.com

## 📞 Support

For issues or questions, please create a GitHub issue in this repository.

---

**Status**: ✅ Production Ready
**Last Updated**: May 4, 2026
**Version**: 1.0
