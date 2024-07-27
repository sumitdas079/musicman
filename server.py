from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from authorization.auth import get_spotify_token

app = FastAPI()

# Route to get an artist's information
@app.get("/artist/{artist_id}", response_class=JSONResponse)
async def get_artist(artist_id: str):
    token = await get_spotify_token()
    artist_response = await httpx.get(
        f"https://api.spotify.com/v1/artists/{artist_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    if artist_response.status_code == 200:
        return artist_response.json()
    else:
        raise HTTPException(status_code=artist_response.status_code, detail="Failed to fetch artist information")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
