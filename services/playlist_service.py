from services.auth_service import AuthService
import requests
from dotenv import load_dotenv
from pathlib import Path
import os

class PlaylistService:
    def __init__(self):
        self.auth_service = AuthService()


    def get_all_playlist(self):
        url = "https://api.spotify.com/v1/me/playlists"

        # 003 - 2026-06-14 01:27:26 - Se pagina playlists usando token OAuth de usuario
        # params = {
        #     # "q": artist_name,
        #     # "type": "artist",
        #     "limit": 10,
        #     "offset": 5,
        #     # "market": self.market            
        # }
        #
        # response = requests.get(url, headers=self.get_access_token(), params=params, timeout=15)
        # response.raise_for_status()
        #
        # # return response.json()
        # data = response.json()
        # print(data)
        # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
        # user_access_token = os.getenv("SPOTIFY_USER_ACCESS_TOKEN")
        # if not user_access_token:
        #     raise ValueError("Falta SPOTIFY_USER_ACCESS_TOKEN en .env para consultar playlists del usuario")
        #
        # headers = {
        #     "Authorization": f"Bearer {user_access_token}"
        # }
        headers = self.auth_service.get_user_access_token()

        playlists = []
        limit = 10
        offset = 0

        while True:
            params = {
                "limit": limit,
                "offset": offset
            }

            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            playlists.extend(items)

            if not items or not data.get("next"):
                break

            offset += limit

        return playlists