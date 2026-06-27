from entities.temaikenfy import Temaikenfy
from router.command_router import CommandRouter
import requests
from rich.console import Console
from rich.table import Table
from util.utils import get_help_commands


def main():
    app = Temaikenfy()
    app_2 = CommandRouter()

    while True:
        command = input("temaikenfy> ").strip()
        command_name = command.split(maxsplit=1)[0].lower() if command else ""

        if command_name == "exit":
            break

        # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
        # if command.startswith("artista"):
        if command_name == "help":
            app_2.help_command()
        elif command_name == "login":
            # app.login_user()
            app_2.dispatch("login")
            print("Login realizado correctamente")
        elif command_name == "info":
            app_2.dispatch(command)
            # # nombre = command.replace("artista ", "", 1)
            # # JP 16/06/2026 - Control para determinar si se ingreso el comando + el nombre del artista.
            # command_parts = command.split(maxsplit=1)            
            # nombre = command_parts[1].strip() if len(command_parts) > 1 else ""     
            # if not nombre:
            #     print("No se ingreso el nombre del artista que se quiere buscar.")
            #     continue      

            # artist = app.buscar_artista(nombre)                        
            # if not artist:
            #     print(f"No encontré el artista: {nombre}")
            #     return

            # print()
            # # print(f"Artista: {artist['name']}")
            # # print(f"ID: {artist.get('id', 'N/D')}")
            # # JP 16/06/2026 - Formateo de info de artista.
            # format_data(
            #     data=[artist],
            #     title=f"Info de {nombre}",
            #     columns=[
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         {
            #             "header": "Spotify",                        
            #             "style": "green",
            #             "value": lambda artist: artist.get("external_urls", {}).get("spotify", "N/D")
            #         },                    
            #         {"header": "ID", "key": "id", "style": "magenta"}
            #     ]
            # )            
            # print()
        elif command_name == "albums":
            app_2.dispatch(command)
            
            # # nombre = command.replace("albums ", "", 1)            
            # # JP 16/06/2026 - Control para determinar si se ingreso el comando + el nombre del artista.
            # command_parts = command.split(maxsplit=1)
            # nombre = command_parts[1].strip() if len(command_parts) > 1 else ""     
            # if not nombre:
            #     print("No se ingreso el nombre del artista.")
            #     continue

            # # albums = app.srch_albums(nombre)
            # if not albums:
            #     print(f"No encontré los album del artista: {nombre}")
            #     return

            # # 001 - 2026-06-13 21:12:34 - Se agrega formatter dinamico con Rich para albums
            # # print()
            # # print(f"Albums de {nombre}:")
            # # for album in albums:
            # #     print(f"- {album.get('name', 'N/D')}")
            # print()
            # format_data(
            #     data=albums,
            #     title=f"Albums de {nombre}",
            #     columns=[
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         {
            #             "header": "Año de lanzamiento",
            #             "style": "green",
            #             "value": lambda album: album.get("release_date", "N/D")[:4],
            #         },
            #         {"header": "Canciones", "key": "total_tracks", "style": "magenta"},
            #         {"header": "ID", "style": "red", "value": lambda album: album.get("id", "N/D")}
            #     ]
            # )
            # print()
        elif command_name == "tracks": 
            app_2.dispatch(command)
            # # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
            # # id_album = command.replace("tracks ", "", 1)
            # command_parts = command.split(maxsplit=1)
            # id_album = command_parts[1].strip() if len(command_parts) > 1 else ""
            # # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
            # # if id_album is None:
            # if not id_album:
            #     print("No se ingreso el id del albums")
            #     continue

            # albums_tracks = app.srch_album_track(id_album)            
            # if not albums_tracks:
            #     print(f"No encontré las canciones del id: {id_album}")
            #     return    
            
            # # print(albums_tracks)
            
            # print()
            # format_data(
            #     data=albums_tracks,
            #     title=f"Albums de {id_album}",
            #     columns=[
            #         {"header": "Nro.", "key": "track_number", "style": "cyan"},
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         {
            #             "header": "Duración",
            #             "style": "green",
            #             # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
            #             # "value": lambda ms: f"{int((ms.get("duration_ms", "N/D") / 1000) // 60)}:{int(round((ms.get("duration_ms", "N/D") / 1000) % 60)):02d}", #Convierto los ms en minutos.
            #             "value": lambda track: f"{int((track.get('duration_ms', 0) / 1000) // 60)}:{int(round((track.get('duration_ms', 0) / 1000) % 60)):02d}", #Convierto los ms en minutos.
                        
            #         }
            #     ]
            # ) 
            # print()
        elif command_name == "playlist-all":
            app_2.dispatch(command)     
            # command_parts = command.split(maxsplit=1)
            # sec_command = command_parts[1].strip() if len(command_parts) > 1 else ""
            # if sec_command.lower().startswith("get-all"):
            #     # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
            #     # app.get_all_playlist()
            #     playlists = app.get_all_playlist()
            #     print()
            #     format_data(
            #         data=playlists,
            #         title="Playlists",
            #         columns=[
            #             {"header": "Nombre", "key": "name", "style": "cyan"},
            #             {
            #                 "header": "Owner",
            #                 "style": "green",
            #                 "value": lambda playlist: playlist.get("Creador", {}).get("display_name", "N/D"),
            #             },
            #             {
            #                 "header": "Tracks",
            #                 "style": "magenta",
            #                 # 006 - 2026-06-14 19:18:11 - Se obtiene total de canciones desde tracks o items en playlists
            #                 # "value": lambda playlist: playlist.get("tracks", {}).get("total", "N/D")
            #                 "value": lambda playlist: (playlist.get("tracks") or playlist.get("items") or {}).get("total", "N/D")
            #             },
            #             {
            #                 "header": "Colaborativa",
            #                 "style": "yellow",
            #                 "value": lambda playlist: "Si" if playlist.get("collaborative", "N/D") == True else "No"
            #             },                        
            #             {"header": "ID", "key": "id", "style": "red"},
            #         ]
            #     )
            #     print()
        # 007 - 2026-06-17 17:47:05 - Se controla status sin usuario logueado
        # elif command.startswith("status"): 
        elif command_name == "status": 
            app_2.dispatch(command)
            # # 007 - 2026-06-17 17:47:05 - Se controla status sin usuario logueado
            # # user = app.get_status()  
            # try:
            #     user = app.get_status()
            # except ValueError as error:
            #     print()
            #     print(error)
            #     print()
            #     continue

            # if not user:
            #     print()
            #     print("No hay ningun usuario logueado. Ejecuta el comando: login")
            #     print()
            #     continue

            # print()
            # format_data(
            #     data=[user],
            #     title=f"Usuario conectado:",
            #     columns=[
            #         {"header": "Usuario", "key": "id","style": "cyan"},
            #         {"header": "Nombre", "key": "display_name", "style": "green"},
            #         {
            #             "header": "Spotify",
            #             "style": "magenta",
            #             "value": lambda user: user.get("external_urls", {}).get("spotify", "N/D"),
            #         },                                                                       
            #         {
            #             "header": "Seguidores",
            #             "style": "yellow",
            #             "value": lambda user: user.get("followers", {}).get("total", "N/D"),
            #         },                    
            #     ]
            # )  
            # print()
        # 009 - 2026-06-17 22:34:06 - Se agrega soporte para top items del usuario
        # elif command_name == "top-tracks":
        elif command_name == "top-tracks":
            app_2.dispatch(command)
            # try:
            #     top_tracks = app.get_top_items("tracks")
            # except ValueError as error:
            #     print()
            #     print(error)
            #     print()
            #     continue
            # except requests.exceptions.HTTPError as error:
            #     print()
            #     if error.response is not None and error.response.status_code == 403:
            #         print("No tenes permisos para leer tus tops. Agrega user-top-read a SPOTIFY_USER_SCOPES y ejecuta login nuevamente.")
            #     else:
            #         print(error)
            #     print()
            #     continue

            # if not top_tracks:
            #     print()
            #     print("No se encontraron tracks en tus tops.")
            #     print()
            #     continue

            # print()
            # format_data(
            #     data=top_tracks,
            #     title="Top canciones",
            #     columns=[
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         {
            #             "header": "Artista",
            #             "style": "green",
            #             "value": lambda track: ", ".join([artist.get("name", "N/D") for artist in track.get("artists", [])]),
            #         },
            #         {
            #             "header": "Album",
            #             "style": "magenta",
            #             "value": lambda track: track.get("album", {}).get("name", "N/D"),
            #         },
            #     ],
            # )
            # print()
        elif command_name == "top-artists":
            app_2.dispatch("top-artists")
            # try:
            #     top_artists = app.get_top_items("artists")
            # except ValueError as error:
            #     print()
            #     print(error)
            #     print()
            #     continue
            # except requests.exceptions.HTTPError as error:
            #     print()
            #     if error.response is not None and error.response.status_code == 403:
            #         print("No tenes permisos para leer tus tops. Agrega user-top-read a SPOTIFY_USER_SCOPES y ejecuta login nuevamente.")
            #     else:
            #         print(error)
            #     print()
            #     continue

            # if not top_artists:
            #     print()
            #     print("No se encontraron artistas en tus tops.")
            #     print()
            #     continue

            # print()
            # format_data(
            #     data=top_artists,
            #     title="Top artistas",
            #     columns=[
            #         {"header": "Nombre", "key": "name", "style": "cyan"},
            #         # {
            #         #     "header": "Generos",
            #         #     "style": "green",
            #         #     "value": lambda artist: ", ".join(artist.get("genres", [])) if artist.get("genres") else "N/D",
            #         # },
            #         # {"header": "Popularidad", "key": "popularity", "style": "yellow"},
            #         # {"header": "ID", "key": "id", "style": "red"},
            #     ],
            # )
            # print()
        elif command_name == "my-tracks":
            app_2.dispatch(command)
        elif command_name == "player-state":
            app_2.dispatch(command)
        elif command_name == "devices":
            app_2.dispatch(command) 
        elif command_name == "play-device":
            app_2.dispatch(command)
        elif command_name == "transfer-playback":
            app_2.dispatch(command)
        elif command_name == "current-track":
            app_2.dispatch(command)
        elif command_name == "pause":
            app_2.dispatch(command)
        elif command_name == "next-track":
            app_2.dispatch(command)
        elif command_name == "previous-track":
            app_2.dispatch(command)
        elif command_name == "volume":
            app_2.dispatch(command)
        elif command_name == "shuffle":
            app_2.dispatch(command)
        elif command_name == "recently-played":
            app_2.dispatch(command)
        elif command_name == "queue":
            app_2.dispatch(command)
        elif command_name == "add-queue":
            app_2.dispatch(command)                       
        else:
            print()
            print("Comando no reconocido. Utilice 'help' para ver todos los comandos disponibles.")
            print()

# 001 - 2026-06-13 21:12:34 - Se agrega formatter dinamico con Rich para albums
# def format_data(data, columns, title="Resultados"):
    
#     console = Console()

#     # table = Table(title="Personas")
#     # table.add_column("Nombre", style="cyan", no_wrap=True)
#     # table.add_column("Apellido", style="cyan")
#     #
#     # table.add_row("Juan", "Perez")
#     # table.add_row("Maria", "Gomez")
#     # table.add_row("Lucia", "Fernandez")
#     # table.add_row("Carlos", "Rodriguez")
#     table = Table(title=title)

#     # Esto recorre las columnas que se envian desde el llamado y extrae los encabezados. Ademas del color.
#     for column in columns:
#         table.add_column(column["header"], style=column.get("style", "white"))


#     for item in data:
#         row = []
#         for column in columns:
#             value_getter = column.get("value")
#             if value_getter:
#                 value = value_getter(item)
#             else:
#                 value = item.get(column.get("key"), "N/D")
#             row.append(str(value))

#         table.add_row(*row)

#     console.print(table)

# def help_command():
#     # 008 - 2026-06-17 18:12:32 - Se mueve objeto de help a utils
#     # obj = [
#     #     {
#     #         "command": "help",
#     #         "description": "Muestra el listado de comandos disponibles.",
#     #         "usage": "help",
#     #     },
#     #     {
#     #         "command": "login",
#     #         "description": "Inicia sesion en Spotify.",
#     #         "usage": "login",
#     #     },
#     #     {
#     #         "command": "status",
#     #         "description": "Muestra el usuario conectado.",
#     #         "usage": "status",
#     #     },
#     #     {
#     #         "command": "info",
#     #         "description": "Busca un artista por nombre.",
#     #         "usage": "info <nombre del artista>",
#     #     },
#     #     {
#     #         "command": "albums",
#     #         "description": "Obtiene los albums de un artista.",
#     #         "usage": "albums <nombre del artista>",
#     #     },
#     #     {
#     #         "command": "tracks",
#     #         "description": "Obtiene las canciones de un album por ID.",
#     #         "usage": "tracks <id del album>",
#     #     },
#     #     {
#     #         "command": "playlist get-all",
#     #         "description": "Obtiene todas las playlists del usuario autenticado.",
#     #         "usage": "playlist get-all",
#     #     },
#     #     {
#     #         "command": "exit",
#     #         "description": "Finaliza la aplicacion.",
#     #         "usage": "exit",
#     #     },
#     # ]
#     obj = get_help_commands()

#     format_data(
#         data=obj,
#         title="Comandos disponibles",
#         columns=[
#             {"header": "Comando", "key": "command", "style": "cyan"},
#             {"header": "Descripcion", "key": "description", "style": "green"},
#             {"header": "Uso", "key": "usage", "style": "magenta"},
#         ],
#     )


if __name__ == "__main__":
    main()
