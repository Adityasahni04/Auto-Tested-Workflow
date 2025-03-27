import requests
import time

API_URL = "http://localhost:8000"  # Update to container URL if needed

# Define test cases
testcases = [
    {"url": f"{API_URL}/add/2/2", "expected": 4, "description": "Test addition of 2 and 2"},
    {"url": f"{API_URL}/subtract/2/2", "expected": 0, "description": "Test subtraction of 2 from 2"},
    {"url": f"{API_URL}/multiply/2/2", "expected": 4, "description": "Test multiplication of 2 and 2"},
]

def test():
    """Runs automated tests on the API endpoints."""
    
    # Wait for the API to start
    time.sleep(5)  # Ensures the API is running before sending requests
    
    for case in testcases:
        response = requests.get(case["url"])
        result = response.json().get("result")

        assert result == case["expected"], f"Test failed: {case['description']}. Expected {case['expected']}, got {result}"
        print(f"✅ Test passed: {case['description']}")

    print("🎉 All tests passed!")

# Run the test function
if __name__ == "__main__":
    test()
