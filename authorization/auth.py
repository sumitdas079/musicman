import os
import requests
import httpx, base64, traceback
from fastapi import HTTPException

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Spotify API credentials
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify API token
# SPOTIFY_TOKEN = None

def get_spotify_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    headers = {
        'Authorization' : f"Basic {auth_base64}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type' : 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        print(f"Access Token: {access_token}")
        return access_token
    else:
        # print(f"Failed to get access token: {response,status_code}")
        traceback.print_exc()
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate")
        print(response.json())
        return None

    
def main():
    try:
        token = get_spotify_token()
        if token:
            print("Token retrieved")
        else:
            print("Failed to receive token")
    except Exception as e:
        traceback.print_exc()
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()