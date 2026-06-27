from services.playlist_service import PlaylistService
from printers import DataPrinter

class PlaylistController:
    def __init__(self):
        self.playlist_service = PlaylistService()
        self.printer = DataPrinter()

    def all_playlist(self):
        playlist_all = self.playlist_service.get_all_playlist()

        if not playlist_all:
            print(f"No se encontraron playlist")
            return

        self.printer.format_data(
                data=playlist_all,
                title="Playlists",
                columns=[
                    {"header": "Nombre", "key": "name", "style": "cyan"},
                    {
                        "header": "Owner",
                        "style": "green",
                        "value": lambda playlist: playlist.get("Creador", {}).get("display_name", "N/D"),
                    },
                    {
                        "header": "Tracks",
                        "style": "magenta",
                        "value": lambda playlist: (playlist.get("tracks") or playlist.get("items") or {}).get("total", "N/D")
                    },
                    {
                        "header": "Colaborativa",
                        "style": "yellow",
                        "value": lambda playlist: "Si" if playlist.get("collaborative", "N/D") == True else "No"
                    },                        
                    {"header": "ID", "key": "id", "style": "red"},
                ]
            )     