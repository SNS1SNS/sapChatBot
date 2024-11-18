import requests
import os
from dotenv import load_dotenv



load_dotenv()

AICORE_AUTH_URL = os.getenv('AICORE_AUTH_URL')
AICORE_CLIENT_ID = os.getenv('AICORE_CLIENT_ID')
AICORE_CLIENT_SECRET = os.getenv('AICORE_CLIENT_SECRET')
DEPLOYMENT_ID = os.getenv('DEPLOYMENT_ID')
def get_embedding(text):
    auth_response = requests.post(
        f"{AICORE_AUTH_URL}/oauth/token",
        data={
            'grant_type': 'client_credentials',
            'client_id': AICORE_CLIENT_ID,
            'client_secret': AICORE_CLIENT_SECRET
        }
    )

    if auth_response.status_code == 200:
        token = auth_response.json().get("access_token")
    else:
        print("Ошибка при получении токена:", auth_response.status_code, auth_response.text)
        return None

    deployment_id = DEPLOYMENT_ID
    headers = {
        "Authorization": f"Bearer {token}",
        "AI-Resource-Group": "default",
        "Content-Type": "application/json"
    }

    invoke_payload = {"input": text}

    response = requests.post(deployment_id, headers=headers, json=invoke_payload)

    if response.status_code == 200:
        model_response = response.json()
        embedding_data = model_response['data'][0]['embedding']
        return embedding_data
    else:
        print("Ошибка при вызове модели:", response.status_code, response.text)
        return None

