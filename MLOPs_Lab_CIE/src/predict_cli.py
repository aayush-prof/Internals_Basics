import argparse
import json
import joblib
import numpy as np
from pathlib import Path
import os
import sys

def load_model():
    """Load the best trained model"""
    model_files = list(Path("models").glob("best_model_*.pkl"))
    if not model_files:
        raise FileNotFoundError("No trained model found in models/ directory. Run train.py first.")
    model_path = model_files[0]
    return joblib.load(model_path), str(model_path)

def predict(severity_level, alerts_count, analyst_experience, is_automated):
    """Make prediction with loaded model"""
    try:
        model, model_path = load_model()
        
        # Prepare input as 2D array
        input_data = np.array([[
            severity_level,
            alerts_count,
            analyst_experience,
            is_automated
        ]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return {
            "image_name": "shieldops-predictor",
            "image_tag": "v1",
            "base_image": "python:3.11-slim",
            "test_input": {
                "severity_level": severity_level,
                "alerts_count": alerts_count,
                "analyst_experience": analyst_experience,
                "is_automated": is_automated
            },
            "prediction": float(prediction)
        }
    except Exception as e:
        print(f"Error during prediction: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Predict resolution hours for security incidents"
    )
    parser.add_argument(
        "--severity_level",
        type=int,
        required=True,
        help="Severity level (1-10)"
    )
    parser.add_argument(
        "--alerts_count",
        type=int,
        required=True,
        help="Number of alerts (1-100)"
    )
    parser.add_argument(
        "--analyst_experience",
        type=int,
        required=True,
        help="Analyst experience in years (1-20)"
    )
    parser.add_argument(
        "--is_automated",
        type=int,
        required=True,
        help="Is response automated? (0 or 1)"
    )
    
    args = parser.parse_args()
    
    result = predict(
        args.severity_level,
        args.alerts_count,
        args.analyst_experience,
        args.is_automated
    )
    
    print(json.dumps(result, indent=2))
