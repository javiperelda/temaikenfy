from entities.temaikenfy import Temaikenfy
from rich.console import Console
from rich.table import Table


def main():
    app = Temaikenfy()

    while True:
        command = input("temaikenfy> ").strip()

        if command == "exit":
            break

        # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
        # if command.startswith("artista"):
        if command == "login":
            app.login_user()
            print("Login realizado correctamente")
        elif command.startswith("artista"):
            nombre = command.replace("artista ", "", 1)
            artist = app.buscar_artista(nombre)
            print(artist)
            if not artist:
                print(f"No encontré el artista: {nombre}")
                return

            print()
            print(f"Artista: {artist['name']}")
            print(f"ID: {artist.get('id', 'N/D')}")
            print()
        elif command.startswith("albums"):
            nombre = command.replace("albums ", "", 1)
            albums = app.srch_albums(nombre)
            # 001 - 2026-06-13 21:12:34 - Se agrega formatter dinamico con Rich para albums
            # print(albums)
            if not albums:
                print(f"No encontré los album del artista: {nombre}")
                return

            # 001 - 2026-06-13 21:12:34 - Se agrega formatter dinamico con Rich para albums
            # print()
            # print(f"Albums de {nombre}:")
            # for album in albums:
            #     print(f"- {album.get('name', 'N/D')}")
            # print()
            format_data(
                data=albums,
                title=f"Albums de {nombre}",
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
        elif command.startswith("tracks"): 
            # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
            # id_album = command.replace("tracks ", "", 1)
            command_parts = command.split(maxsplit=1)
            id_album = command_parts[1].strip() if len(command_parts) > 1 else ""
            # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
            # if id_album is None:
            if not id_album:
                print("No se ingreso el id del albums")
                continue

            albums_tracks = app.srch_album_track(id_album)            
            if not albums_tracks:
                print(f"No encontré las canciones del id: {id_album}")
                return    
            
            format_data(
                data=albums_tracks,
                title=f"Albums de {id_album}",
                columns=[
                    {"header": "Nro.", "key": "track_number", "style": "cyan"},
                    {"header": "Nombre", "key": "name", "style": "cyan"},
                    {
                        "header": "Duración",
                        "style": "green",
                        # 002 - 2026-06-14 00:35:42 - Se valida argumento requerido para comando tracks
                        # "value": lambda ms: f"{int((ms.get("duration_ms", "N/D") / 1000) // 60)}:{int(round((ms.get("duration_ms", "N/D") / 1000) % 60)):02d}", #Convierto los ms en minutos.
                        "value": lambda track: f"{int((track.get('duration_ms', 0) / 1000) // 60)}:{int(round((track.get('duration_ms', 0) / 1000) % 60)):02d}", #Convierto los ms en minutos.
                        
                    }
                ]
            ) 
        elif command.startswith("playlist"):     
            command_parts = command.split(maxsplit=1)
            sec_command = command_parts[1].strip() if len(command_parts) > 1 else ""
            if sec_command.startswith("get-all"):
                # 004 - 2026-06-14 01:34:55 - Se agrega login OAuth PKCE con refresh token
                # app.get_all_playlist()
                playlists = app.get_all_playlist()
                format_data(
                    data=playlists,
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
                            # 006 - 2026-06-14 19:18:11 - Se obtiene total de canciones desde tracks o items en playlists
                            # "value": lambda playlist: playlist.get("tracks", {}).get("total", "N/D")
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
        else:
            print("command no reconocido")

# 001 - 2026-06-13 21:12:34 - Se agrega formatter dinamico con Rich para albums
def format_data(data, columns, title="Resultados"):
    
    console = Console()

    # table = Table(title="Personas")
    # table.add_column("Nombre", style="cyan", no_wrap=True)
    # table.add_column("Apellido", style="cyan")
    #
    # table.add_row("Juan", "Perez")
    # table.add_row("Maria", "Gomez")
    # table.add_row("Lucia", "Fernandez")
    # table.add_row("Carlos", "Rodriguez")
    table = Table(title=title)

    # Esto recorre las columnas que se envian desde el llamado y extrae los encabezados. Ademas del color.
    for column in columns:
        table.add_column(column["header"], style=column.get("style", "white"))


    for item in data:
        row = []
        for column in columns:
            value_getter = column.get("value")
            if value_getter:
                value = value_getter(item)
            else:
                value = item.get(column.get("key"), "N/D")
            row.append(str(value))

        table.add_row(*row)

    console.print(table)

if __name__ == "__main__":
    main()
