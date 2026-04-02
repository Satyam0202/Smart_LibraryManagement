import requests
import json

url = "http://localhost:5000/populate_sample_data"

print("Sending request to populate 100 sample books...")
print("-" * 60)

response = requests.post(url)
data = response.json()

print(f"Status: {data.get('status')}")
print(f"Message: {data.get('message')}")
if 'count' in data:
    print(f"Total books added: {data.get('count')}")
if 'added' in data:
    print(f"Successfully added: {data.get('added')}")
if 'failed' in data:
    print(f"Failed to add: {data.get('failed')}")
    
print("-" * 60)
print("Full response:")
print(json.dumps(data, indent=2))
