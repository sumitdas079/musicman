import os
import httpx
from fastapi import HTTPException

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify API token
SPOTIFY_TOKEN = None

async def get_spotify_token():
    global SPOTIFY_TOKEN
    if SPOTIFY_TOKEN is None:
        auth_response = await httpx.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "client_credentials"
            },
            headers={
                "Authorization": f"Basic {httpx.util.to_bytes(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}')}"
            }
        )
        if auth_response.status_code == 200:
            SPOTIFY_TOKEN = auth_response.json().get("access_token")
        else:
            raise HTTPException(status_code=500, detail="Failed to authenticate with Spotify API")
    return SPOTIFY_TOKEN
