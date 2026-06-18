def get_help_commands():
    return [
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
            "command": "playlist get-all",
            "description": "Obtiene todas las playlists del usuario autenticado.",
            "usage": "playlist get-all",
        },
        # 009 - 2026-06-17 22:34:06 - Se agrega soporte para top items del usuario
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
            "command": "exit",
            "description": "Finaliza la aplicacion.",
            "usage": "exit",
        },
    ]
