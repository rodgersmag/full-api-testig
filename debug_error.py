import requests
import json

# Test the POST /users/ endpoint
url = "http://localhost:8000/users/"
data = {
    "email": "newuser@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "password": "StrongPassword!1"
}

print("Testing POST /users/")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
