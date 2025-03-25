import base64
import requests

CLIENT_ID = "<CLIENT_ID>"
CLIENT_SECRET = "<CLIENT_SECRET>"


def get_access_token(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_credentials}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://auth.tidal.com/v1/oauth2/token", headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# Example usage
access_token_response = get_access_token(CLIENT_ID, CLIENT_SECRET)
print(access_token_response)