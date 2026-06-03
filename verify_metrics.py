from fastapi.testclient import TestClient
from src import app

client = TestClient(app)

def test_metrics():
    # Make a few requests to populate metrics
    client.get("/health")
    client.get("/")
    client.get("/non_existent_route")
    
    # Get metrics
    response = client.get("/metrics")
    assert response.status_code == 200
    metrics_output = response.text
    
    # Assert metrics contain our custom counters and histograms
    assert "http_requests_total" in metrics_output
    assert "http_request_duration_seconds" in metrics_output
    
    # Check that Python runtime metrics are there
    assert "python_gc_objects_collected_total" in metrics_output
    
    print("Metrics verification successful!")
    print(f"Metrics output snippet:\n{metrics_output[:500]}...")

if __name__ == "__main__":
    test_metrics()
