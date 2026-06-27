from router.command_router import CommandRouter
from database import init_db

def main():    

    init_db() # Inicializa la base de datos SQLite.

    app = CommandRouter()
    list_commands = {
        "help",
        "login",
        "status",
        "info",
        "albums",
        "tracks",
        "playlist-all",
        "top-tracks",
        "top-artists",
        "my-tracks",
        "player-state",
        "devices",
        "play-device",
        "transfer-playback",
        "current-track",
        "pause",
        "next-track",
        "previous-track",
        "volume",
        "shuffle",
        "recently-played",
        "queue",
        "add-queue",
        "exit",
    }

    while True:
        command = input("temaikenfy> ").strip() # Esto permite que siempre se muestre el prefijo 'temaikenfy>' en la consola.
        # Esta linea corta la primera palabra que se ingresa, la cual corresponde al comando asi luego validarlo.
        command_name = command.split(maxsplit=1)[0].lower() if command else ""

        if command_name == "exit":
            break

        if command_name == "help":
            app.help_command()
        # Para no repetir IF y controlar por cada uno de los comandos. Controla si el comando ingresado esta dentro de la lista de comandos disponibles.
        elif command_name in list_commands:
            app.dispatch(command) # Llama al disptach del controlador pasandole el comando ingresado.
        else:
            print()
            print("Comando no reconocido. Utilice 'help' para ver todos los comandos disponibles.")
            print()


if __name__ == "__main__":
    main()
