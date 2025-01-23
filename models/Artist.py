from pydantic import BaseModel
from typing import List

class Artist(BaseModel):
    name: str
    genres: List[str]
    followers: List[str]