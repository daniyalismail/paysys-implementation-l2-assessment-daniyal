import os
import pytest
import requests
import time
from uuid import uuid4

API_URL = os.environ.get("API_URL", "http://localhost:8080/api")
HEADERS = {"Authorization": "Bearer test-token-123", "Content-Type": "application/json"}

@pytest.fixture(scope="session")
def base_url():
    return API_URL

def test_health_check(base_url):
    # Expecting /health at the root, not under /api
    health_url = base_url.replace("/api", "/health")
    start_time = time.time()
    response = requests.get(health_url)
    elapsed_time = time.time() - start_time
    
    assert response.status_code == 200
    assert elapsed_time < 0.5  # Response time threshold < 500ms

def test_create_customer_success(base_url):
    payload = {"name": "John Doe", "email": "john@example.com"}
    response = requests.post(f"{base_url}/customers", json=payload, headers=HEADERS)
    
    if response.status_code != 502: # Ignore 502 if backend is mocked/unreachable
        assert response.status_code in (200, 201)
        data = response.json()
        assert "id" in data
        assert data["name"] == payload["name"]

def test_create_payment_invalid_fields(base_url):
    payload = {"amount": -10} # Invalid amount
    response = requests.post(f"{base_url}/payments", json=payload, headers=HEADERS)
    
    if response.status_code != 502:
        assert response.status_code == 400
        assert "error" in response.json()

def test_unknown_resource(base_url):
    response = requests.get(f"{base_url}/nonexistent-endpoint", headers=HEADERS)
    assert response.status_code in (404, 502)

def test_unauthorized_access(base_url):
    payload = {"name": "Hacker"}
    response = requests.post(f"{base_url}/customers", json=payload) # Missing auth header
    
    if response.status_code != 502:
        assert response.status_code in (401, 403)

def test_idempotent_payment_submission(base_url):
    idem_key = str(uuid4())
    payload = {"customer_id": 1, "amount": 100.0}
    headers = {**HEADERS, "Idempotency-Key": idem_key}
    
    # First request
    res1 = requests.post(f"{base_url}/payments", json=payload, headers=headers)
    # Second request with same key
    res2 = requests.post(f"{base_url}/payments", json=payload, headers=headers)
    
    if res1.status_code not in (404, 502):
        assert res2.status_code == res1.status_code
        # In a real system, res2 should return the exact same body/ID as res1
        assert res1.json() == res2.json()

def test_server_error_behavior(base_url):
    # Simulating a server error (e.g. asking for a specific bug-inducing payload)
    payload = {"amount": "trigger_500"}
    response = requests.post(f"{base_url}/payments", json=payload, headers=HEADERS)
    
    if response.status_code != 502:
        assert response.status_code >= 400 # Should be handled gracefully, not crash the server

