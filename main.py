from entities.temaikenfy import Temaikenfy
from rich.console import Console
from rich.table import Table


def main():
    app = Temaikenfy()
    # print(app._headers())

    # console = Console()

    # table = Table(title="Personas")
    # table.add_column("Nombre", style="cyan", no_wrap=True)
    # table.add_column("Apellido", style="cyan")

    # table.add_row("Juan", "Perez")
    # table.add_row("Maria", "Gomez")
    # table.add_row("Lucia", "Fernandez")
    # table.add_row("Carlos", "Rodriguez")

    # console.print(table)

    
    # print(app.search_artist("laspastillas"))

    while True:
        comando = input("temaikenfy> ").strip()

        if comando == "salir":
            break

        if comando.startswith("buscar artista "):
            nombre = comando.replace("buscar artista ", "", 1)
            artist = app.buscar_artista(nombre)
            print(artist)
            if not artist:
                print(f"No encontré el artista: {nombre}")
                return

            print()
            print(f"Artista: {artist['name']}")
            print(f"ID: {artist.get('id', 'N/D')}")
            print()
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    main()
