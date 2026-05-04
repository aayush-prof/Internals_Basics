import requests
import json
import random
from datetime import datetime
from pathlib import Path
import time

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

BASE_URL = "http://localhost:9000"

def send_request(severity_level, alerts_count, analyst_experience, is_automated):
    """Send a prediction request to the API"""
    payload = {
        "severity_level": severity_level,
        "alerts_count": alerts_count,
        "analyst_experience": analyst_experience,
        "is_automated": is_automated
    }
    try:
        response = requests.post(f"{BASE_URL}/infer", json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending request: {e}")
        return False

def generate_normal_requests(count=40):
    """Generate normal requests (similar to training distribution)"""
    requests_data = []
    severity_levels = [1, 2, 3, 4, 5]
    
    for _ in range(count):
        severity = random.choice(severity_levels)
        alerts = random.randint(5, 50)
        experience = random.randint(5, 18)
        automated = random.choice([0, 1])
        
        requests_data.append({
            "severity_level": severity,
            "alerts_count": alerts,
            "analyst_experience": experience,
            "is_automated": automated
        })
    
    return requests_data

def generate_drifted_requests(count=10):
    """Generate drifted requests (anomalies)"""
    requests_data = []
    
    for _ in range(count):
        # Drifted: high severity, high alerts, low experience
        severity = random.randint(7, 10)
        alerts = random.randint(70, 100)
        experience = random.randint(1, 3)
        automated = 0
        
        requests_data.append({
            "severity_level": severity,
            "alerts_count": alerts,
            "analyst_experience": experience,
            "is_automated": automated
        })
    
    return requests_data

if __name__ == "__main__":
    print("Starting traffic simulation...")
    print("="*50)
    
    # Generate requests
    normal_requests = generate_normal_requests(40)
    drifted_requests = generate_drifted_requests(10)
    all_requests = normal_requests + drifted_requests
    
    # Shuffle to interleave
    random.shuffle(all_requests)
    
    print(f"Sending {len(all_requests)} total requests:")
    print(f"  - {len(normal_requests)} normal requests")
    print(f"  - {len(drifted_requests)} drifted requests")
    print()
    
    successful = 0
    failed = 0
    
    for i, req in enumerate(all_requests, 1):
        success = send_request(
            req["severity_level"],
            req["alerts_count"],
            req["analyst_experience"],
            req["is_automated"]
        )
        
        if success:
            successful += 1
            status_str = "✓"
        else:
            failed += 1
            status_str = "✗"
        
        print(f"[{i:2d}/50] {status_str} Severity: {req['severity_level']}, "
              f"Alerts: {req['alerts_count']}, Experience: {req['analyst_experience']}, "
              f"Automated: {req['is_automated']}")
        
        time.sleep(0.1)  # Small delay between requests
    
    print()
    print("="*50)
    print(f"Simulation complete!")
    print(f"Successful: {successful}/50")
    print(f"Failed: {failed}/50")
    print("="*50)
