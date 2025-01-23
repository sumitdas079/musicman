from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from icecream import ic
import httpx, traceback
import uvicorn
from authorization.auth import get_spotify_token

app = FastAPI()

# Route to get an artist's information
@app.get("/artist/{artist_id}", response_class=JSONResponse)
def get_artist(artist_id: str):
    artist_info = {}
    token = get_spotify_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    artist_response = httpx.get(
        f"https://api.spotify.com/v1/artists/{artist_id}", headers = headers
    )
    if artist_response.status_code == 200:
        response = artist_response.json()
        ic(response)
        # print("Artist name: ", response["name"])
        artist_info = {
            "Artist": response["name"],
            "Followers": response["followers"]["total"],
            "Genre": response["genres"]
        }
        print("Artist info: ", artist_info)
        return response
    else:
        traceback.print_exc()
        raise HTTPException(status_code=artist_response.status_code, detail="Failed to fetch artist information")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
