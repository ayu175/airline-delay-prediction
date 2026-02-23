import pytest
from fastapi.testclient import TestClient
from delay_prediction_api import app

client = TestClient(app)

def test_welcome_endpoint():
    """Test the welcome endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This API is functional."}

def test_predict_delays_valid_request():
    """Test prediction endpoint with valid parameters."""
    response = client.get(
        "/predict/delays",
        params={
            "DEST_AIRPORT": "10785",  # from airport_encodings.json
            "DEPARTURE_TIME": "2024-08-15T14:00:00",
            "ARRIVAL_TIME": "2024-08-15T17:00:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "average_departure_delay_minutes" in data
    assert isinstance(data["average_departure_delay_minutes"], (int, float))

def test_predict_delays_invalid_requests():
    """Test prediction endpoint with various invalid parameters."""
    
    # Test 1: Invalid airport code
    response = client.get(
        "/predict/delays",
        params={
            "DEST_AIRPORT": "INVALID_AIRPORT",
            "DEPARTURE_TIME": "2024-08-15T14:00:00",
            "ARRIVAL_TIME": "2024-08-15T17:00:00"
        }
    )
    assert response.status_code == 404
    assert "Arrival airport not found" in response.json()["detail"]
    
    # Test 2: Invalid datetime format
    response = client.get(
        "/predict/delays",
        params={
            "DEST_AIRPORT": "10785",  # Valid airport from encodings
            "DEPARTURE_TIME": "invalid-datetime",
            "ARRIVAL_TIME": "2024-08-15T17:00:00"
        }
    )
    assert response.status_code == 400
    assert "Invalid datetime format" in response.json()["detail"]
    
    # Test 3: Missing required parameters
    response = client.get(
        "/predict/delays",
        params={
            "DEST_AIRPORT": "10785"
            # Missing DEPARTURE_TIME and ARRIVAL_TIME
        }
    )
    assert response.status_code == 422
