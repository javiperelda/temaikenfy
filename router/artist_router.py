from services.artist_service import ArtistService
from printers import DataPrinter

class ArtistController:
    def __init__(self):
        self.artist_service = ArtistService()
        self.printer = DataPrinter()

    def albums(self, params):
        albums = self.artist_service.srch_albums(params)

        if not albums:
            print(f"No se encontraron albums para {params}")
            return

        self.printer.format_data(
            data=albums,
            title=f"Albums de {params}",
            columns=[
                {"header": "Nombre", "key": "name", "style": "cyan"},
                {
                    "header": "Año de lanzamiento",
                    "style": "green",
                    "value": lambda album: album.get("release_date", "N/D")[:4],
                },
                {"header": "Canciones", "key": "total_tracks", "style": "magenta"},
                {"header": "ID", "style": "red", "value": lambda album: album.get("id", "N/D")}
            ]
        )
    
    def album_tracks(self, params):
        album_tracks = self.artist_service.srch_album_track(params)

        if not album_tracks:
            print(f"No se encontraron canciones para el album {params}")
            return

        self.printer.format_data(
            data=album_tracks,
            title=f"Tracks del album {params}",
            columns=[
                {"header": "Nro.", "key": "track_number", "style": "cyan"},
                {"header": "Nombre", "key": "name", "style": "cyan"},
                {
                    "header": "Duración",
                    "style": "green",
                    "value": lambda track: f"{int((track.get('duration_ms', 0) / 1000) // 60)}:{int(round((track.get('duration_ms', 0) / 1000) % 60)):02d}", #Convierto los ms en minutos.
                    
                },                
                {"header": "ID", "key": "id", "style": "red", "no_wrap": True, "overflow": "ignore"}
            ]
        ) 

    def info(self, params):
        info_artist = self.artist_service.buscar_artista(params)

        if not info_artist:
            print(f"No se encontraron canciones para el album {params}")
            return
        
        self.printer.format_data(
            data=[info_artist],
            title=f"Info de {params}",
            columns=[
                {"header": "Nombre", "key": "name", "style": "cyan"},
                {
                    "header": "Spotify",                        
                    "style": "green",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda artist: artist.get("external_urls", {}).get("spotify", "N/D")
                },                    
                {"header": "ID", "key": "id", "style": "magenta"}
            ]
        )             
