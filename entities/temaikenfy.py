from dotenv import load_dotenv
import os
import time
import requests
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Temaikenfy:
    def __init__(self):    
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.market = os.getenv("SPOTIFY_MARKET", "AR")

        self.access_token = None
        self.token_expires_at = 0

        if not self.client_id or not self.client_secret:
            raise ValueError("Faltan SPOTIFY_CLIENT_ID o SPOTIFY_CLIENT_SECRET en el archivo .env")

    def validate_token(self):
        return self.access_token is not None and time.time() < self.token_expires_at

    def token(self):
        url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=data, headers=headers, timeout=15)
        response.raise_for_status()

        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.token_expires_at = time.time() + token_data["expires_in"] - 60

        return self.access_token

    def get_access_token(self):
        if self.validate_token():
            return self.access_token

        return self.token()

    def bearer_token(self):
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}"
        }
    
    def buscar_artista(self, artist_name):
        url = "https://api.spotify.com/v1/search"

        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1,
            "market": self.market
        }

        response = requests.get(url, headers=self.bearer_token(), params=params, timeout=15)
        response.raise_for_status()

        # return response.json()
        data = response.json()
        artists = data.get("artists", {}).get("items", [])

        if not artists:
            return None

        return artists[0]
