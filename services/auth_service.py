from dotenv import load_dotenv
# 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
import base64
import hashlib
import http.server
import json
import os
import secrets
import time
import requests
import urllib.parse
import webbrowser
from pathlib import Path


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)
# 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
TOKEN_CACHE_PATH = Path(__file__).resolve().parent.parent / "auth" / "token_cache.json"

class AuthService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.market = os.getenv("SPOTIFY_MARKET", "AR")
        # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
        # 009 - 2026-06-17 22:34:06 - Se agrega soporte para top items del usuario
        # self.user_scopes = os.getenv("SPOTIFY_USER_SCOPES", "playlist-read-private playlist-read-collaborative")
        self.user_scopes = os.getenv("SPOTIFY_USER_SCOPES", "playlist-read-private playlist-read-collaborative user-top-read")

        self.access_token = None
        self.token_expires_at = 0

        if not self.client_id or not self.client_secret:
            raise ValueError("Faltan SPOTIFY_CLIENT_ID o SPOTIFY_CLIENT_SECRET en el archivo .env")    

    # ----------------------------------------------------------------------------------------------------
    # OBTENER TOKEN

    # Se llama al endpoint para obtener el token. Antes de retornarlo al metodo que lo llama, se valida que
    # no haya expirado. Si es valido, retorna el token; si no, vuelve a generarlo. Luego arma el bearer token.
    # ----------------------------------------------------------------------------------------------------

    # def bearer_token(token):
    #     # Arma el formato del bearer token.
    #     return {
    #         "Authorization": f"Bearer {token}"
    #     }

    # def exec_command(self, command):
    #     if command == "login":
    #         self.login_user()                    
                        

    def get_access_token(self):
        if time.time() < self.token_expires_at:
            token = self.access_token
        else:
            token = self.get_token()

        return {
            "Authorization": f"Bearer {token}"
        }

    def get_token(self):
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
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 005 - 2026-06-14 10:47:47 - Se documenta bloque de login OAuth PKCE
    # LOGIN OAUTH PKCE
    # Este bloque maneja el login de usuario contra Spotify para endpoints privados como /me/playlists.
    # Genera el code_verifier/code_challenge, abre el navegador, recibe el callback local, guarda tokens
    # en auth/token_cache.json y renueva el access_token usando refresh_token cuando expira.
    # ----------------------------------------------------------------------------------------------------

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def get_user_access_token(self):
        token_data = self.load_user_token_cache()

        if token_data and time.time() < token_data.get("expires_at", 0):
            return {
                "Authorization": f"Bearer {token_data['access_token']}"
            }

        if token_data and token_data.get("refresh_token"):
            token_data = self.refresh_user_token(token_data["refresh_token"])
            return {
                "Authorization": f"Bearer {token_data['access_token']}"
            }

        raise ValueError("No hay login de usuario. Ejecuta el comando: login")

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def login_user(self):
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        state = secrets.token_urlsafe(16)

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": self.user_scopes,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }

        auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
        print("Abriendo navegador para iniciar sesion con Spotify...")
        webbrowser.open(auth_url)

        callback_params = self.wait_for_login_callback()

        if callback_params.get("state") != state:
            raise ValueError("El state recibido no coincide con el state enviado")

        code = callback_params.get("code")
        if not code:
            error = callback_params.get("error", "No se recibio code de Spotify")
            raise ValueError(error)

        token_data = self.exchange_code_for_user_token(code, code_verifier)
        self.save_user_token_cache(token_data)

        return token_data

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def generate_code_verifier(self):
        return secrets.token_urlsafe(64)

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def generate_code_challenge(self, code_verifier):
        code_digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_digest).decode("utf-8")
        return code_challenge.rstrip("=")

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def wait_for_login_callback(self):
        parsed_redirect = urllib.parse.urlparse(self.redirect_uri)
        callback_data = {}

        class SpotifyCallbackHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(handler_self):
                parsed_path = urllib.parse.urlparse(handler_self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)

                callback_data.update({
                    key: values[0]
                    for key, values in query_params.items()
                })

                handler_self.send_response(200)
                handler_self.send_header("Content-type", "text/html")
                handler_self.end_headers()
                handler_self.wfile.write(b"<h1>Login completo</h1><p>Ya podes volver a la consola.</p>")

            def log_message(self, format, *args):
                return

        server_address = (parsed_redirect.hostname, parsed_redirect.port)
        with http.server.HTTPServer(server_address, SpotifyCallbackHandler) as server:
            print(f"Esperando callback en {self.redirect_uri}...")
            server.handle_request()

        return callback_data

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def exchange_code_for_user_token(self, code, code_verifier):
        url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "code_verifier": code_verifier,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=data, headers=headers, timeout=15)
        response.raise_for_status()

        return self.prepare_user_token_data(response.json())

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def refresh_user_token(self, refresh_token):
        url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=data, headers=headers, timeout=15)
        response.raise_for_status()

        token_data = response.json()
        if "refresh_token" not in token_data:
            token_data["refresh_token"] = refresh_token

        token_data = self.prepare_user_token_data(token_data)
        self.save_user_token_cache(token_data)

        return token_data

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def prepare_user_token_data(self, token_data):
        token_data["expires_at"] = time.time() + token_data["expires_in"] - 60
        return token_data

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def load_user_token_cache(self):
        if not TOKEN_CACHE_PATH.exists():
            return None

        with open(TOKEN_CACHE_PATH, "r", encoding="utf-8") as token_file:
            return json.load(token_file)

    # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
    def save_user_token_cache(self, token_data):
        TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(TOKEN_CACHE_PATH, "w", encoding="utf-8") as token_file:
            json.dump(token_data, token_file, indent=4)

    # ----------------------------------------------------------------------------------------------------
    # 005 - 2026-06-14 10:47:47 - Se documenta bloque de login OAuth PKCE
    # FIN LOGIN OAUTH PKCE
    # ----------------------------------------------------------------------------------------------------        