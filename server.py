from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from icecream import ic
import httpx, traceback
import uvicorn
from authorization.auth import get_spotify_token
from models import Artist

app = FastAPI()

# Route to get an artist's information
@app.get("/artist/{artist_id}", response_class=Artist)
async def get_artist(artist_id: str):
    try:
        artist_info = {}
        token = get_spotify_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = httpx.get(
            f"https://api.spotify.com/v1/artists/{artist_id}", headers = headers
        )
        # url = f"https://api.spotify.com/v1/artists/{artist_id}"
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(url, headers=headers)

        if response.status_code == 200:
            artist_response = response.json()
            ic(artist_response)
            # print("Artist name: ", response["name"])
            # artist_info = {
            #     "Artist": response["name"],
            #     "Followers": response["followers"]["total"],
            #     "Genre": response["genres"]
            # }
            artist_info = Artist(
                name=artist_response["name"],
                followers=artist_response["followers"]["total"],
                genres=artist_response["genres"]
            )
            print("Artist info: ", artist_info)
            return artist_response
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch artist information")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
