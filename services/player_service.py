import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from services.auth_service import AuthService

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class PlayerService:
    def __init__(self):
        self.auth_service = AuthService()
        self.market = os.getenv("SPOTIFY_MARKET", "AR") 
    
    # Obtiene el estado actual del reproductor del usuario: dispositivo activo, cancion, progreso, shuffle y repeat.
    def get_playback_state(self):
        url = "https://api.spotify.com/v1/me/player"

        params = {
            "market": self.market,
            "additional_types": "track,episode"
        }

        response = requests.get(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        if response.status_code == 204:
            return None

        response.raise_for_status()
        data = response.json()

        return data
    
    # Transfiere la reproduccion a un dispositivo especifico de Spotify.
    def set_transfer_playback(self, device_id, play=False):
        url = "https://api.spotify.com/v1/me/player"

        data = {
            "device_ids": [device_id],
            "play": play
        }

        response = requests.put(url, headers=self.auth_service.get_user_access_token(), json=data, timeout=15)
        response.raise_for_status()

        return True
    
    # Lista los dispositivos disponibles del usuario.
    def get_devices(self):
        url = "https://api.spotify.com/v1/me/player/devices"

        response = requests.get(url, headers=self.auth_service.get_user_access_token(), timeout=15)
        response.raise_for_status()

        data = response.json()
        devices = data.get("devices", [])
        if not devices:
            return None

        return devices
    
    # Obtiene el contenido que se esta reproduciendo.
    def get_current_track(self):
        url = "https://api.spotify.com/v1/me/player/currently-playing"

        params = {
            "market": self.market,
            "additional_types": "track,episode"
        }

        response = requests.get(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        if response.status_code == 204:
            return None

        response.raise_for_status()
        return response.json()
    
    # Inicia o reanuda la reproduccion; permite enviar contexto, lista de URIs, offset y posicion inicial.
    def set_start_playback(self, device_id=None, context_uri=None, uris=None, offset=None, position_ms=None):
        url = "https://api.spotify.com/v1/me/player/play"

        params = {}
        if device_id:
            params["device_id"] = device_id

        data = {}
        if context_uri:
            data["context_uri"] = context_uri
        if uris:
            data["uris"] = uris
        if offset:
            data["offset"] = offset
        if position_ms is not None:
            data["position_ms"] = position_ms

        response = requests.put(
            url,
            headers=self.auth_service.get_user_access_token(),
            params=params,
            json=data if data else None,
            timeout=15
        )
        response.raise_for_status()

        return True
    
    # Pausa la reproduccion actual en el dispositivo.
    def set_pause_playback(self, device_id=None):
        url = "https://api.spotify.com/v1/me/player/pause"

        params = {}
        if device_id:
            params["device_id"] = device_id

        response = requests.put(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
    
    # Salta al siguiente track de la cola del reproductor.
    def next_track(self, device_id=None):
        url = "https://api.spotify.com/v1/me/player/next"

        params = {}
        if device_id:
            params["device_id"] = device_id

        response = requests.post(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
    
    # Vuelve al track anterior del reproductor.
    def previous_track(self, device_id=None):
        url = "https://api.spotify.com/v1/me/player/previous"

        params = {}
        if device_id:
            params["device_id"] = device_id

        response = requests.post(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
    
    # Ajusta el volumen del reproductor en un porcentaje entre 0 y 100.
    def set_volumen(self, volume_percent, device_id=None):
        if volume_percent < 0 or volume_percent > 100:
            raise ValueError("El volumen debe estar entre 0 y 100")

        url = "https://api.spotify.com/v1/me/player/volume"

        params = {
            "volume_percent": volume_percent
        }
        if device_id:
            params["device_id"] = device_id

        response = requests.put(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
    
    # Activa o desactiva el modo aleatorio del reproductor.
    def set_random_track(self, state=True, device_id=None):
        url = "https://api.spotify.com/v1/me/player/shuffle"

        params = {
            "state": state
        }
        if device_id:
            params["device_id"] = device_id

        response = requests.put(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
    
    # Obtiene los tracks reproducidos recientemente.
    def get_recently_tracks(self):
        url = "https://api.spotify.com/v1/me/player/recently-played"

        params = {
            "limit": 10
        }

        response = requests.get(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        items = data.get("items", [])
        if not items:
            return None

        return items
    
    # Obtiene la cola actual del reproductor y lo que se esta reproduciendo.
    def get_queue(self):
        url = "https://api.spotify.com/v1/me/player/queue"

        response = requests.get(url, headers=self.auth_service.get_user_access_token(), timeout=15)
        response.raise_for_status()

        return response.json()
    
    # Agrega un track o episodio a la cola de reproduccion.
    def add_track_queue(self, uri, device_id=None):
        url = "https://api.spotify.com/v1/me/player/queue"

        params = {
            "uri": uri
        }
        if device_id:
            params["device_id"] = device_id

        response = requests.post(url, headers=self.auth_service.get_user_access_token(), params=params, timeout=15)
        response.raise_for_status()

        return True
