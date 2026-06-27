import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from services.auth_service import AuthService

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class ArtistService:
    def __init__(self):
        self.auth_service = AuthService()
        self.market = os.getenv("SPOTIFY_MARKET", "AR")        

    def buscar_artista(self, artist_name):
        url = "https://api.spotify.com/v1/search"

        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1,
            "market": self.market
        }

        response = requests.get(url, headers=self.auth_service.get_access_token(), params=params, timeout=15)
        response.raise_for_status()

        # return response.json()
        data = response.json()
        artists = data.get("artists", {}).get("items", [])

        if not artists:
            return None

        return artists[0]

    def srch_artist(self, artist_name):
        url = "https://api.spotify.com/v1/search"

        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1,
            "market": self.market
        }

        response = requests.get(url, headers=self.auth_service.get_access_token(), params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        artists = data.get("artists", {}).get("items", [])

        if not artists:
            return None

        artist = artists[0].get("id", "N/D")

        return artist

    def srch_albums(self, artist_name):
        id_artist = self.srch_artist(artist_name)
        if not id_artist:
            return None

        url = f"https://api.spotify.com/v1/artists/{id_artist}/albums"    

        # def get_albums_page(offset=0, albums=None):
        band = True
        offset = 0
        albums = None
        while band:
            if albums is None:
                albums = []

            limit = 10
            params = {
                "include_groups": "album",
                "limit": limit,
                "offset": offset,
                "market": self.market
            }

            response = requests.get(url, headers=self.auth_service.get_access_token(), params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            albums.extend(items)

            offset += limit
            
            if not items or not data.get("next"):
                # return albums
                # band = False
                break
            

            # return get_albums_page(offset + limit, albums)

        # albums = get_albums_page()

        if not albums:
            return None

        return albums
    
    def srch_album_track(self, id_album):
        url = f"https://api.spotify.com/v1/albums/{id_album}/tracks"

        params = {            
            # "type": "artist",
            "limit": 15,
            "market": self.market
        }

        response = requests.get(url, headers=self.auth_service.get_access_token(), params=params, timeout=15)
        response.raise_for_status()

        tracks = None
        if tracks is None:
            tracks = []        

        data = response.json()        
        items = data.get("items", [])
        tracks.extend(items)        

        return tracks                 