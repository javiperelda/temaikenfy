from printers import DataPrinter
from services.player_service import PlayerService
class PlayerController:
    def __init__(self):
        self.player_service = PlayerService()
        self.printer = DataPrinter()
    
    def playback_state(self):
        state = self.player_service.get_playback_state()

        if not state:
            print("No hay reproduccion activa.")
            return

        self.printer.format_data(
            data=[state],
            title="Estado del reproductor",
            columns=[
                {
                    "header": "Estado",
                    "style": "green",
                    "value": lambda item: "Reproduciendo" if item.get("is_playing") else "Pausado",
                },
                {
                    "header": "Cancion",
                    "style": "cyan",
                    "value": lambda item: item.get("item", {}).get("name", "N/D"),
                },
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda item: ", ".join([
                        artist.get("name", "N/D")
                        for artist in item.get("item", {}).get("artists", [])
                    ]),
                },
                {
                    "header": "Album",
                    "style": "magenta",
                    "value": lambda item: item.get("item", {}).get("album", {}).get("name", "N/D"),
                },
                {
                    "header": "Progreso",
                    "style": "yellow",
                    "value": lambda item: (
                        f"{int((item.get('progress_ms', 0) / 1000) // 60)}:"
                        f"{int((item.get('progress_ms', 0) / 1000) % 60):02d} / "
                        f"{int((item.get('item', {}).get('duration_ms', 0) / 1000) // 60)}:"
                        f"{int((item.get('item', {}).get('duration_ms', 0) / 1000) % 60):02d}"
                    ),
                },
                {
                    "header": "Dispositivo",
                    "style": "blue",
                    "value": lambda item: item.get("device", {}).get("name", "N/D"),
                },
                {
                    "header": "Volumen",
                    "style": "cyan",
                    "value": lambda item: f"{item.get('device', {}).get('volume_percent', 'N/D')}%",
                },
                {
                    "header": "Shuffle",
                    "style": "yellow",
                    "value": lambda item: "Si" if item.get("shuffle_state") else "No",
                },
                {
                    "header": "Repeat",
                    "key": "repeat_state",
                    "style": "magenta",
                },
            ],
        )


    def devices(self):
        devices = self.player_service.get_devices()

        if not devices:
            print("No hay dispositivos disponibles.")
            return

        self.printer.format_data(
            data=devices,
            title="Dispositivos disponibles",
            columns=[
                {"header": "Nombre", "key": "name", "style": "cyan"},
                {"header": "Tipo", "key": "type", "style": "green"},
                {
                    "header": "Activo",
                    "style": "yellow",
                    "value": lambda device: "Si" if device.get("is_active") else "No",
                },
                {
                    "header": "Volumen",
                    "style": "magenta",
                    "value": lambda device: f"{device.get('volume_percent', 'N/D')}%",
                },
                {
                    "header": "Soporta volumen",
                    "style": "green",
                    "value": lambda device: "Si" if device.get("supports_volume") else "No",
                },
                {
                    "header": "Sesion privada",
                    "style": "yellow",
                    "value": lambda device: "Si" if device.get("is_private_session") else "No",
                },
                {
                    "header": "Restringido",
                    "style": "red",
                    "value": lambda device: "Si" if device.get("is_restricted") else "No",
                },
                {
                    "header": "ID",
                    "key": "id",
                    "style": "blue",
                    "no_wrap": True,
                    "overflow": "ignore",
                },
            ],
        )
    
    def set_start_playback(self, params="", device_id=None):
        spotify_uri = params.strip() if params else ""
        context_uri = None
        uris = None

        if spotify_uri:
            if spotify_uri.startswith("spotify:track:") or spotify_uri.startswith("spotify:episode:"):
                uris = [spotify_uri]
            else:
                context_uri = spotify_uri

        started = self.player_service.set_start_playback(            
            device_id=device_id,
            context_uri=context_uri,
            uris=uris,
            position_ms=0
        )

        if not started:
            print("No se pudo iniciar la reproduccion.")
            return

        if spotify_uri:
            print(f"Reproduccion iniciada para: {spotify_uri}")
        else:
            print("Reproduccion iniciada.")
    
    def set_start_playback_device(self, params=""):
        command_parts = params.split(maxsplit=1)
        device_id = command_parts[0].strip() if len(command_parts) > 0 else ""
        spotify_uri = command_parts[1].strip() if len(command_parts) > 1 else ""

        if not device_id:
            print("No se ingreso el id del dispositivo.")
            return

        self.set_start_playback(spotify_uri, device_id=device_id)
    
    def transfer_playback(self, params=""):
        command_parts = params.split(maxsplit=1)
        device_id = command_parts[0].strip() if len(command_parts) > 0 else ""
        play_param = command_parts[1].strip().lower() if len(command_parts) > 1 else "false"

        if not device_id:
            print("No se ingreso el id del dispositivo.")
            return

        transferred = self.player_service.set_transfer_playback(
            device_id=device_id,
            play=play_param in ["true", "si", "1", "play"]
        )

        if not transferred:
            print("No se pudo transferir la reproduccion.")
            return

        print(f"Reproduccion transferida al dispositivo: {device_id}")
    
    def current_track(self):
        current = self.player_service.get_current_track()

        if not current:
            print("No hay una cancion reproduciendose actualmente.")
            return

        self.printer.format_data(
            data=[current],
            title="Cancion actual",
            columns=[
                {
                    "header": "Estado",
                    "style": "green",
                    "value": lambda item: "Reproduciendo" if item.get("is_playing") else "Pausado",
                },
                {
                    "header": "Cancion",
                    "style": "cyan",
                    "value": lambda item: item.get("item", {}).get("name", "N/D"),
                },
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda item: ", ".join([
                        artist.get("name", "N/D")
                        for artist in item.get("item", {}).get("artists", [])
                    ]),
                },
                {
                    "header": "Album",
                    "style": "magenta",
                    "value": lambda item: item.get("item", {}).get("album", {}).get("name", "N/D"),
                },
                {
                    "header": "Progreso",
                    "style": "yellow",
                    "value": lambda item: (
                        f"{int((item.get('progress_ms', 0) / 1000) // 60)}:"
                        f"{int((item.get('progress_ms', 0) / 1000) % 60):02d} / "
                        f"{int((item.get('item', {}).get('duration_ms', 0) / 1000) // 60)}:"
                        f"{int((item.get('item', {}).get('duration_ms', 0) / 1000) % 60):02d}"
                    ),
                },
                {
                    "header": "Spotify",
                    "style": "blue",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda item: item.get("item", {}).get("external_urls", {}).get("spotify", "N/D"),
                },
                {
                    "header": "ID",
                    "style": "red",
                    "no_wrap": True,
                    "overflow": "ignore",
                    "value": lambda item: item.get("item", {}).get("id", "N/D"),
                },
            ],
        )
    
    def pause_playback(self, params=""):
        device_id = params.strip() if params else None
        paused = self.player_service.set_pause_playback(device_id=device_id)

        if not paused:
            print("No se pudo pausar la reproduccion.")
            return

        print("Reproduccion pausada.")
    
    def next_track(self, params=""):
        device_id = params.strip() if params else None
        skipped = self.player_service.next_track(device_id=device_id)

        if not skipped:
            print("No se pudo pasar a la siguiente cancion.")
            return

        print("Paso a la siguiente cancion.")
    
    def previous_track(self, params=""):
        device_id = params.strip() if params else None
        skipped = self.player_service.previous_track(device_id=device_id)

        if not skipped:
            print("No se pudo volver a la cancion anterior.")
            return

        print("Paso a la cancion anterior.")
    
    def set_volume(self, params=""):
        command_parts = params.split(maxsplit=1)
        volume = command_parts[0].strip() if len(command_parts) > 0 else ""
        device_id = command_parts[1].strip() if len(command_parts) > 1 else None

        if not volume:
            print("No se ingreso el volumen.")
            return

        changed = self.player_service.set_volumen(
            volume_percent=int(volume),
            device_id=device_id
        )

        if not changed:
            print("No se pudo cambiar el volumen.")
            return

        print(f"Volumen actualizado a {volume}%.")
    
    def shuffle(self, params=""):
        command_parts = params.split(maxsplit=1)
        state_param = command_parts[0].strip().lower() if len(command_parts) > 0 else "true"
        device_id = command_parts[1].strip() if len(command_parts) > 1 else None
        state = state_param in ["true", "si", "1", "on"]

        changed = self.player_service.set_random_track(
            state=state,
            device_id=device_id
        )

        if not changed:
            print("No se pudo cambiar el modo aleatorio.")
            return

        print(f"Modo aleatorio {'activado' if state else 'desactivado'}.")
    
    def recently_played(self):
        items = self.player_service.get_recently_tracks()

        if not items:
            print("No se encontraron canciones reproducidas recientemente.")
            return

        self.printer.format_data(
            data=items,
            title="Reproducidas recientemente",
            columns=[
                {
                    "header": "Cancion",
                    "style": "cyan",
                    "value": lambda item: item.get("track", {}).get("name", "N/D"),
                },
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda item: ", ".join([
                        artist.get("name", "N/D")
                        for artist in item.get("track", {}).get("artists", [])
                    ]),
                },
                {
                    "header": "Album",
                    "style": "magenta",
                    "value": lambda item: item.get("track", {}).get("album", {}).get("name", "N/D"),
                },
                {
                    "header": "Reproducida",
                    "style": "yellow",
                    "value": lambda item: item.get("played_at", "N/D")[:19],
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
    
    def queue(self):
        queue_data = self.player_service.get_queue()

        if not queue_data:
            print("No se pudo obtener la cola de reproduccion.")
            return

        currently_playing = queue_data.get("currently_playing")
        queue_items = queue_data.get("queue", [])

        if currently_playing:
            self.printer.format_data(
                data=[currently_playing],
                title="Reproduciendo ahora",
                columns=[
                    {"header": "Cancion", "key": "name", "style": "cyan"},
                    {
                        "header": "Artista",
                        "style": "green",
                        "value": lambda item: ", ".join([
                            artist.get("name", "N/D")
                            for artist in item.get("artists", [])
                        ]),
                    },
                    {"header": "ID", "key": "id", "style": "red", "no_wrap": True, "overflow": "ignore"},
                ],
            )

        if not queue_items:
            print("No hay canciones en la cola.")
            return

        self.printer.format_data(
            data=queue_items,
            title="Cola de reproduccion",
            columns=[
                {"header": "Cancion", "key": "name", "style": "cyan"},
                {
                    "header": "Artista",
                    "style": "green",
                    "value": lambda item: ", ".join([
                        artist.get("name", "N/D")
                        for artist in item.get("artists", [])
                    ]),
                },
                {
                    "header": "Album",
                    "style": "magenta",
                    "value": lambda item: item.get("album", {}).get("name", "N/D"),
                },
                {"header": "ID", "key": "id", "style": "red", "no_wrap": True, "overflow": "ignore"},
            ],
        )

    def add_track_queue(self, params=""):
        command_parts = params.split(maxsplit=1)
        uri = command_parts[0].strip() if len(command_parts) > 0 else ""
        device_id = command_parts[1].strip() if len(command_parts) > 1 else None

        if not uri:
            print("No se ingreso la URI para agregar a la cola.")
            return

        added = self.player_service.add_track_queue(
            uri=uri,
            device_id=device_id
        )

        if not added:
            print("No se pudo agregar a la cola.")
            return

        print(f"Agregado a la cola: {uri}")
