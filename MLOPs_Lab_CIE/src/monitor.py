import json
import pandas as pd
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
    
    # Extract input features
    inputs = [p["input"] for p in predictions]
    df = pd.DataFrame(inputs)
    
    # Calculate statistics
    mean_severity = df["severity_level"].mean()
    mean_alerts = df["alerts_count"].mean()
    mean_experience = df["analyst_experience"].mean()
    mean_automated = df["is_automated"].mean()
    
    # Training data statistics (from train.py)
    train_mean_severity = 2.8  # Approximate from training data
    train_mean_alerts = 33.5   # Approximate from training data
    
    # Detect drifts
    alerts = []
    
    # Severity drift detection
    severity_diff = abs(mean_severity - train_mean_severity)
    if severity_diff > SEVERITY_THRESHOLD:
        alerts.append({
            "type": "SEVERITY_DRIFT",
            "current_mean": float(mean_severity),
            "threshold": SEVERITY_THRESHOLD,
            "diff": float(severity_diff),
            "status": "ALERT"
        })
    
    # Alerts count drift detection
    alerts_diff = abs(mean_alerts - train_mean_alerts)
    if alerts_diff > ALERTS_THRESHOLD:
        alerts.append({
            "type": "ALERTS_DRIFT",
            "current_mean": float(mean_alerts),
            "threshold": ALERTS_THRESHOLD,
            "diff": float(alerts_diff),
            "status": "ALERT"
        })
    
    return {
        "total_predictions": len(predictions),
        "statistics": {
            "mean_severity_level": float(mean_severity),
            "mean_alerts_count": float(mean_alerts),
            "mean_analyst_experience": float(mean_experience),
            "mean_is_automated": float(mean_automated)
        },
        "drift_detection": {
            "severity_threshold": SEVERITY_THRESHOLD,
            "alerts_threshold": ALERTS_THRESHOLD,
            "alerts": alerts,
            "drift_detected": len(alerts) > 0
        }
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
        
        print("\nStatistics:")
        print(f"  Mean Severity Level: {results['statistics']['mean_severity_level']:.2f}")
        print(f"  Mean Alerts Count: {results['statistics']['mean_alerts_count']:.2f}")
        print(f"  Mean Analyst Experience: {results['statistics']['mean_analyst_experience']:.2f}")
        print(f"  Mean Is Automated: {results['statistics']['mean_is_automated']:.2f}")
        
        print("\nDrift Detection:")
        print(f"  Severity Threshold: {results['drift_detection']['severity_threshold']:.2f}")
        print(f"  Alerts Threshold: {results['drift_detection']['alerts_threshold']:.2f}")
        
        if results['drift_detection']['drift_detected']:
            print(f"\n  ⚠️  DATA DRIFT DETECTED:")
            for alert in results['drift_detection']['alerts']:
                print(f"     - {alert['type']}: Current={alert['current_mean']:.2f}, "
                      f"Threshold={alert['threshold']:.2f}, Diff={alert['diff']:.2f}")
        else:
            print("\n  ✓ No significant drift detected")
        
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
