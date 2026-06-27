from services.user_service import UserService
from printers import DataPrinter


class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.printer = DataPrinter()

    def status(self):
        status = self.user_service.get_status()

        if not status:
            print("No hay ningun usuario logueado. Ejecuta el comando: login")
            return

        self.printer.format_data(
            data=[status],
            title="Usuario conectado:",
            columns=[
                {"header": "Usuario", "key": "id", "style": "cyan"},
                {"header": "Nombre", "key": "display_name", "style": "green"},
                {
                    "header": "Spotify",
                    "style": "magenta",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda user: user.get("external_urls", {}).get("spotify", "N/D"),
                },
                {
                    "header": "Seguidores",
                    "style": "yellow",
                    "value": lambda user: user.get("followers", {}).get("total", "N/D"),
                },
            ],
        )

    def top_tracks(self, params):
        items = self.user_service.get_top_items(params)

        if not items:
            print("No se encontraron tracks en tus tops.")
            return

        self.printer.format_data(
            data=items,
            title="Top canciones",
            columns=[
                {"header": "Nombre", "key": "name", "style": "cyan"},
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda track: ", ".join([artist.get("name", "N/D") for artist in track.get("artists", [])]),
                },
                {
                    "header": "Album",
                    "style": "magenta",
                    "value": lambda track: track.get("album", {}).get("name", "N/D"),
                },
            ],
        )

    def top_artists(self, params):
        items = self.user_service.get_top_items(params)

        if not items:
            print("No se encontraron artistas en tus tops.")
            return

        self.printer.format_data(
            data=items,
            title="Top artistas",
            columns=[
                {"header": "Nombre", "key": "name", "style": "cyan"},
            ],
        )

    def my_tracks(self):
        items = self.user_service.get_my_tracks()

        if not items:
            print("No se encontraron tracks guardados en tu biblioteca.")
            return


        self.printer.format_data(
            data=items,
            title="Tracks de mi biblioteca",
            columns=[
                {
                    "header": "Canción",
                    "style": "cyan",
                    "value": lambda item: item.get("track", {}).get("name", "N/D"),
                },
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda item: ", ".join([artist.get("name", "N/D") for artist in item.get("track", {}).get("artists", [])]),
                },
                {
                    "header": "Álbum",
                    "style": "magenta",
                    "value": lambda item: item.get("track", {}).get("album", {}).get("name", "N/D"),
                },
                {
                    "header": "Duración",
                    "style": "green",
                    "value": lambda item: f"{int((item.get('track', {}).get('duration_ms', 0) / 1000) // 60)}:{int(round((item.get('track', {}).get('duration_ms', 0) / 1000) % 60)):02d}",
                },
                # {
                #     "header": "Agregado",
                #     "style": "yellow",
                #     "value": lambda item: item.get("added_at", "N/D")[:10],
                # },
                {
                    "header": "Spotify",
                    "style": "blue",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda item: item.get("track", {}).get("external_urls", {}).get("spotify", "N/D"),
                },
                {
                    "header": "ID",
                    "style": "red",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda item: item.get("track", {}).get("id", "N/D"),
                },
            ],
        )
