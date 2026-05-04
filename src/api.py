from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import logging

# Configure logging for predictions
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

# Initialize FastAPI app
app = FastAPI(title="ShieldOps Predictor", version="1.0")

# Global model variable
model = None
model_path = None

class PredictionInput(BaseModel):
    severity_level: int = Field(..., ge=1, le=10, description="Severity level 1-10")
    alerts_count: int = Field(..., ge=1, le=100, description="Alert count 1-100")
    analyst_experience: int = Field(..., ge=1, le=20, description="Experience 1-20 years")
    is_automated: int = Field(..., ge=0, le=1, description="Automated response 0 or 1")

class PredictionOutput(BaseModel):
    input: dict
    prediction: float
    model: str
    version: str

class PingResponse(BaseModel):
    status: str
    model: str
    version: str

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model, model_path
    try:
        model_files = list(Path("models").glob("best_model_*.pkl"))
        if not model_files:
            raise FileNotFoundError("No trained model found in models/ directory")
        model_path = model_files[0]
        model = joblib.load(model_path)
        print(f"Model loaded: {model_path}")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

@app.get("/ping", response_model=PingResponse)
async def ping():
    """Health check endpoint"""
    return {
        "status": "running",
        "model": str(model_path),
        "version": "1.0"
    }

@app.post("/infer", response_model=PredictionOutput)
async def infer(input_data: PredictionInput):
    """Make prediction endpoint"""
    try:
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded"
            )
        
        # Prepare input for prediction
        prediction_input = np.array([[
            input_data.severity_level,
            input_data.alerts_count,
            input_data.analyst_experience,
            input_data.is_automated
        ]])
        
        # Make prediction
        prediction = model.predict(prediction_input)[0]
        
        # Log prediction to predictions.jsonl
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input": input_data.dict(),
            "prediction": float(prediction)
        }
        
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)
        
        # Append to JSONL file
        with open("logs/predictions.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return {
            "input": input_data.dict(),
            "prediction": float(prediction),
            "model": str(model_path),
            "version": "1.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
