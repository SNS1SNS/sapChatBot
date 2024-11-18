import requests

base_url = "http://localhost:5000"

response = requests.post(f"{base_url}/get_embedding", json={"text": "Не берут "})
print(response.json())

similar_response = requests.post(f"{base_url}/find_similar", json={"text": "Не берут", "threshold": 0.7})
print(similar_response.json())

update_response = requests.post(f"{base_url}/update_all_vectors")
print(update_response.json())
