from services.auth_service import AuthService
from router.artist_router import ArtistController
from router.playlist_router import PlaylistController
from router.user_router import UserController
from router.player_router import PlayerController
from printers import DataPrinter
import shlex

class CommandRouter:
    def __init__(self):
        self.auth_service = AuthService()
        self.artist_controller = ArtistController()
        self.playlist_controller = PlaylistController()
        self.user_controller = UserController()
        self.player_controller = PlayerController()

        self.printer = DataPrinter()


    def dispatch(self, command):

        args = shlex.split(command)

        command_parts = command.split(maxsplit=1)

        command = command_parts[0].lower().strip()
        params = command_parts[1].strip() if len(command_parts) > 1 else ""       

        if not command:
            return

        if command == "login":        
            # self.auth_service.exec_command(command)
            self.auth_service.login_user()
        elif command == "status":
            self.user_controller.status()
        elif command == "albums": 
            self.artist_controller.albums(params)
        elif command == "tracks":
            self.artist_controller.album_tracks(params)
        elif command =="info":
            self.artist_controller.info(params)
        elif command == "playlist-all":
            self.playlist_controller.all_playlist()
        elif command == "top-tracks":
            self.user_controller.top_tracks("tracks")
        elif command == "top-artists":
            self.user_controller.top_artists("artists")          
        elif command == "my-tracks":
            self.user_controller.my_tracks()  
        elif command == "player-state":
            self.player_controller.playback_state()
        elif command == "devices":
            self.player_controller.devices()                     
        elif command == "play-device":
            self.player_controller.set_start_playback_device(params)
        # 020 - 2026-06-27 12:24:42 - Se implementan metodos restantes del player router
        elif command == "transfer-playback":
            self.player_controller.transfer_playback(params)
        elif command == "current-track":
            self.player_controller.current_track()
        elif command == "pause":
            self.player_controller.pause_playback(params)
        elif command == "next-track":
            self.player_controller.next_track(params)
        elif command == "previous-track":
            self.player_controller.previous_track(params)
        elif command == "volume":
            self.player_controller.set_volume(params)
        elif command == "shuffle":
            self.player_controller.shuffle(params)
        elif command == "recently-played":
            self.player_controller.recently_played()
        elif command == "queue":
            self.player_controller.queue()
        elif command == "add-queue":
            self.player_controller.add_track_queue(params)


    def help_command(self):
        obj = [
            {
                "command": "help",
                "description": "Muestra el listado de comandos disponibles.",
                "usage": "help",
            },
            {
                "command": "login",
                "description": "Inicia sesion en Spotify.",
                "usage": "login",
            },
            {
                "command": "status",
                "description": "Muestra el usuario conectado.",
                "usage": "status",
            },
            {
                "command": "info",
                "description": "Busca un artista por nombre.",
                "usage": "info <nombre del artista>",
            },
            {
                "command": "albums",
                "description": "Obtiene los albums de un artista.",
                "usage": "albums <nombre del artista>",
            },
            {
                "command": "tracks",
                "description": "Obtiene las canciones de un album por ID.",
                "usage": "tracks <id del album>",
            },
            {
                # 010 - 2026-06-21 22:54:52 - Se formatean tracks guardados en biblioteca
                # "command": "playlist get-all",
                "command": "playlist-all",
                "description": "Obtiene todas las playlists del usuario autenticado.",
                "usage": "playlist-all",
            },
            {
                "command": "top-tracks",
                "description": "Obtiene los tracks mas escuchados del usuario autenticado.",
                "usage": "top-tracks",
            },
            {
                "command": "top-artists",
                "description": "Obtiene los artistas mas escuchados del usuario autenticado.",
                "usage": "top-artists",
            },
            {
                "command": "my-tracks",
                "description": "Obtiene los tracks guardados en la biblioteca del usuario autenticado.",
                "usage": "my-tracks",
            },
            {
                "command": "player-state",
                "description": "Muestra el estado actual del reproductor de Spotify.",
                "usage": "player-state",
            },
            {
                "command": "devices",
                "description": "Muestra los dispositivos disponibles para reproducir Spotify.",
                "usage": "devices",
            },
            # 019 - 2026-06-25 20:27:10 - Se deja solo play-device para iniciar playback
            # {
            #     "command": "play",
            #     "description": "Inicia o reanuda la reproduccion en Spotify.",
            #     "usage": "play [spotify_uri]",
            # },
            {
                "command": "play-device",
                "description": "Inicia la reproduccion en un dispositivo. Usar devices para obtener el device_id.",
                "usage": "play-device <device_id> <spotify_uri>",
            },
            # 020 - 2026-06-27 12:24:42 - Se implementan metodos restantes del player router
            {
                "command": "transfer-playback",
                "description": "Transfiere la reproduccion a un dispositivo.",
                "usage": "transfer-playback <device_id> [true|false]",
            },
            {
                "command": "current-track",
                "description": "Muestra la cancion que se esta reproduciendo actualmente.",
                "usage": "current-track",
            },
            {
                "command": "pause",
                "description": "Pausa la reproduccion actual.",
                "usage": "pause [device_id]",
            },
            {
                "command": "next-track",
                "description": "Salta a la siguiente cancion.",
                "usage": "next-track [device_id]",
            },
            {
                "command": "previous-track",
                "description": "Vuelve a la cancion anterior.",
                "usage": "previous-track [device_id]",
            },
            {
                "command": "volume",
                "description": "Cambia el volumen del reproductor.",
                "usage": "volume <0-100> [device_id]",
            },
            {
                "command": "shuffle",
                "description": "Activa o desactiva el modo aleatorio.",
                "usage": "shuffle <on|off> [device_id]",
            },
            {
                "command": "recently-played",
                "description": "Muestra canciones reproducidas recientemente.",
                "usage": "recently-played",
            },
            {
                "command": "queue",
                "description": "Muestra la cola de reproduccion.",
                "usage": "queue",
            },
            {
                "command": "add-queue",
                "description": "Agrega una cancion o episodio a la cola.",
                "usage": "add-queue <spotify_uri> [device_id]",
            },
            {
                "command": "exit",
                "description": "Finaliza la aplicacion.",
                "usage": "exit",
            },
        ]

        self.printer.format_data(
            data=obj,
            title="Comandos disponibles",
            columns=[
                {"header": "Comando", "key": "command", "style": "cyan"},
                {"header": "Descripcion", "key": "description", "style": "green"},
                {"header": "Uso", "key": "usage", "style": "magenta"},
            ],
        )







            # data = self.artist_controller.exec_command(command, params)
            # if not data:
            #     print(f"No se encontraron datos de {params}")

            # self.printers.format_data(                
            #     data=data,
            #     title=f"Albums de {params}",
            #     columns=[
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         {
            #             "header": "Año de lanzamiento",
            #             "style": "green",
            #             "value": lambda album: album.get("release_date", "N/D")[:4],
            #         },
            #         {"header": "Canciones", "key": "total_tracks", "style": "magenta"},
            #         {"header": "ID", "style": "red", "value": lambda album: album.get("id", "N/D")}
            #     ])

            
