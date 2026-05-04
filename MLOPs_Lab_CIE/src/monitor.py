import json
import pandas as pd
import numpy as np
from pathlib import Path

# Thresholds from training data
SEVERITY_THRESHOLD = 0.88  # Mean deviation allowed
ALERTS_THRESHOLD = 12.71   # Mean alerts (will check drift)

def load_predictions():
    """Load predictions from JSONL file"""
    predictions_file = Path("logs/predictions.jsonl")
    
    if not predictions_file.exists():
        raise FileNotFoundError("logs/predictions.jsonl not found. Run simulate_traffic.py first.")
    
    predictions = []
    with open(predictions_file, "r") as f:
        for line in f:
            if line.strip():
                predictions.append(json.loads(line))
    
    return predictions

def analyze_predictions(predictions):
    """Analyze predictions for data drift"""
    
    # Extract input features and predictions
    inputs = [p["input"] for p in predictions]
    preds = [p["prediction"] for p in predictions]
    df = pd.DataFrame(inputs)
    
    # Calculate statistics
    mean_severity = df["severity_level"].mean()
    mean_alerts = df["alerts_count"].mean()
    mean_experience = df["analyst_experience"].mean()
    mean_automated = df["is_automated"].mean()
    mean_prediction = np.mean(preds)
    
    # Training data statistics (calculated from training_data.csv)
    # severity_level mean: (5+2+2+5+2+4+5+5+4+3+1+1+5+2+4+4+1+5+3+5+4+3+5+1+2)/25 = 3.32
    # alerts_count mean: (10+50+46+20+8+17+47+23+9+34+21+36+46+24+22+32+39+44+3+8+36+32+6+21+45)/25 = 27.16
    train_mean_severity = 3.32
    train_mean_alerts = 27.16
    
    # Detect drifts
    alerts = []
    
    # Severity drift detection
    severity_shift = abs(mean_severity - train_mean_severity)
    if severity_shift > SEVERITY_THRESHOLD:
        alerts.append({
            "feature": "severity_level",
            "train_mean": float(train_mean_severity),
            "live_mean": float(mean_severity),
            "shift": float(severity_shift),
            "threshold": SEVERITY_THRESHOLD,
            "status": "ALERT"
        })
    
    # Alerts count drift detection
    alerts_shift = abs(mean_alerts - train_mean_alerts)
    if alerts_shift > ALERTS_THRESHOLD:
        alerts.append({
            "feature": "alerts_count",
            "train_mean": float(train_mean_alerts),
            "live_mean": float(mean_alerts),
            "shift": float(alerts_shift),
            "threshold": ALERTS_THRESHOLD,
            "status": "ALERT"
        })
    
    return {
        "total_predictions": len(predictions),
        "mean_prediction": float(mean_prediction),
        "drift_detected": len(alerts) > 0,
        "alerts": alerts
    }

if __name__ == "__main__":
    print("Starting monitoring analysis...")
    print("="*50)
    
    try:
        # Load predictions
        predictions = load_predictions()
        print(f"Loaded {len(predictions)} predictions from logs/predictions.jsonl")
        
        # Analyze
        results = analyze_predictions(predictions)
        
        print(f"\nTotal Predictions: {results['total_predictions']}")
        print(f"Mean Prediction Value: {results['mean_prediction']:.2f}")
        print(f"Drift Detected: {results['drift_detected']}")
        
        if results['drift_detected']:
            print(f"\n⚠️  DATA DRIFT ALERTS:")
            for alert in results['alerts']:
                print(f"\n  Feature: {alert['feature']}")
                print(f"    Training Mean: {alert['train_mean']:.2f}")
                print(f"    Live Mean: {alert['live_mean']:.2f}")
                print(f"    Shift: {alert['shift']:.2f}")
                print(f"    Threshold: {alert['threshold']:.2f}")
                print(f"    Status: {alert['status']}")
        else:
            print("\n✓ No significant drift detected")
        
        # Save results
        Path("results").mkdir(exist_ok=True)
        with open("results/step4_s5.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*50)
        print("✓ Monitoring results saved to: results/step4_s5.json")
        print("="*50)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the API is running and simulate_traffic.py has been executed.")
