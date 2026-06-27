import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from services.auth_service import AuthService

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class UserService:
    def __init__(self):
        self.auth_service = AuthService()
        self.market = os.getenv("SPOTIFY_MARKET", "AR") 

    def get_status(self):
        
        url = "https://api.spotify.com/v1/me"

        headers = self.auth_service.get_user_access_token()

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json() 
        if not data:
            return None

        return data

    def get_top_items(self, type):
        if type not in ["artists", "tracks"]:
            raise ValueError("El tipo debe ser 'artists' o 'tracks'")

        url = f"https://api.spotify.com/v1/me/top/{type}"

        params = {
            "time_range": "medium_term",
            "limit": 10,
            "offset": 0
        }
        
        headers = self.auth_service.get_user_access_token()

        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        tops = None
        if tops is None:
            tops = []           

        data = response.json()   
        items = data.get("items", [])
        tops.extend(items)    

        if not tops:
            return None

        return tops
    

    def get_my_tracks(self):

        url = "https://api.spotify.com/v1/me/tracks"    
        
        band = True
        offset = 0
        tracks = None
        while band:
            if tracks is None:
                tracks = []

            limit = 10
            params = {                
                "limit": limit,
                "offset": offset,
                "market": self.market
            }

            response = requests.get(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            tracks.extend(items)

            offset += limit
            
            if not items or not data.get("next"):                
                break
            
        if not tracks:
            return None

        return tracks
    