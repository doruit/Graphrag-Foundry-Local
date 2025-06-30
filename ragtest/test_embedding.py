import requests
import json

# Test embedding endpoint
url = "http://localhost:5273/v1/embeddings"
headers = {"Content-Type": "application/json"}
data = {
    "model": "all-minilm-l6-v2",
    "input": "Hello world"  # Test with simple string instead of array
}

response = requests.post(url, headers=headers, json=data)
print(f"Status code: {response.status_code}")
print(json.dumps(response.json(), indent=2))