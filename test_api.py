import pytest
import requests

BASE_URL = "http://localhost:8000"

# Test cases for basic operations
test_cases = [
    ("/add/2/3", {"operation": "addition", "result": 5}, "Addition Test"),
    ("/subtract/10/5", {"operation": "subtraction", "result": 5}, "Subtraction Test"),
    ("/multiply/4/3", {"operation": "multiplication", "result": 12}, "Multiplication Test"),
    ("/add/-5/-3", {"operation": "addition", "result": -8}, "Negative Number Addition Test"),
    ("/multiply/0/10", {"operation": "multiplication", "result": 0}, "Multiplication by Zero Test"),
]

@pytest.mark.parametrize("endpoint, expected_response, description", test_cases)
def test_operations(endpoint, expected_response, description):
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == 200, f"Failed: {description}"
    assert response.json() == expected_response, f"Mismatch: {description}"

# Test invalid inputs
def test_invalid_inputs():
    response = requests.get(BASE_URL + "/add/abc/3")
    assert response.status_code == 422, "Should return validation error"

# Test division by zero (not implemented)
def test_divide_by_zero():
    response = requests.get(BASE_URL + "/divide/5/0")
    assert response.status_code == 404, "Should return 404 Not Found"

# Test fetching calculation history
def test_history():
    response = requests.get(BASE_URL + "/history")
    assert response.status_code == 200, "Failed to fetch history"
    assert isinstance(response.json().get("history"), list), "History should be a list"

if __name__ == "__main__":
    pytest.main(["-v"])
