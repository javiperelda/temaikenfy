# Temaikenfy

Temaikenfy es una aplicacion de consola CLI hecha en Python para interactuar con la API de Spotify. Permite buscar artistas, listar albums y canciones, consultar informacion del usuario autenticado, ver playlists, revisar tops personales, consultar biblioteca guardada y controlar parcialmente el reproductor de Spotify.

## Caracteristicas

- Login con Spotify usando OAuth PKCE.
- Busqueda de artistas por nombre.
- Listado de albums de un artista.
- Listado de tracks de un album.
- Consulta de usuario conectado.
- Consulta de playlists del usuario.
- Consulta de top tracks y top artists.
- Consulta de canciones guardadas en la biblioteca.
- Consulta de estado del reproductor.
- Listado de dispositivos disponibles.
- Control basico del reproductor: play, pause, siguiente, anterior, volumen, shuffle, cola y canciones recientes.

## Tecnologias

- Python 3
- Spotify Web API
- OAuth 2.0 PKCE
- SQLite
- Requests
- Python Dotenv
- Rich

## Instalacion

1. Clonar el repositorio.

```bash
git clone https://github.com/tu-usuario/temaikenfy.git
cd temaikenfy
```

2. Crear y activar un entorno virtual.

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Instalar dependencias.

```bash
pip install -r requirements.txt
```

## Configuracion

Crear un archivo `.env` en la raiz del proyecto con las credenciales de tu app de Spotify:

```env
# Client ID de la aplicacion creada en Spotify Developer Dashboard.
SPOTIFY_CLIENT_ID=tu_client_id

# Client Secret de la aplicacion creada en Spotify Developer Dashboard.
SPOTIFY_CLIENT_SECRET=tu_client_secret

# URL de callback configurada en Spotify para completar el login OAuth.
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

# Mercado usado para filtrar resultados disponibles por pais.
SPOTIFY_MARKET=AR

# Permisos solicitados al usuario para playlists, biblioteca, tops y player.
SPOTIFY_USER_SCOPES=playlist-read-private playlist-read-collaborative user-top-read user-library-read user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-recently-played

# Carpeta donde se crea/guarda la base SQLite local.
TEMAIKENFY_DB_PATH=./data

# Nombre del archivo SQLite local.
TEMAIKENFY_DB_NAME=temaikenfy.sqlite
```

En el dashboard de Spotify Developer, configurar el mismo Redirect URI:

```text
http://127.0.0.1:8888/callback
```

## Uso

Ejecutar la aplicacion:

```bash
python main.py
```

La consola queda esperando comandos:

```text
temaikenfy>
```

Antes de usar comandos privados del usuario, iniciar sesion:

```bash
login
```

Para ver todos los comandos disponibles:

```bash
help
```

## Persistencia

Temaikenfy utiliza SQLite para almacenar informacion local de autenticacion, como el token de Spotify obtenido durante el login. Esto permite reutilizar la sesion y renovar el acceso sin tener que iniciar sesion manualmente en cada ejecucion.

La ubicacion de la base se configura con estas variables:

```env
TEMAIKENFY_DB_PATH=./data
TEMAIKENFY_DB_NAME=temaikenfy.sqlite
```

SQLite forma parte de la biblioteca estandar de Python, por eso no requiere una dependencia adicional en `requirements.txt`.

## Comandos

### Generales

| Comando | Uso | Descripcion |
| --- | --- | --- |
| `help` | `help` | Muestra el listado de comandos disponibles. |
| `login` | `login` | Inicia sesion con Spotify. |
| `exit` | `exit` | Finaliza la aplicacion. |

### Artistas y albums

| Comando | Uso | Descripcion |
| --- | --- | --- |
| `info` | `info <nombre del artista>` | Busca informacion basica de un artista. |
| `albums` | `albums <nombre del artista>` | Obtiene albums de un artista. |
| `tracks` | `tracks <id del album>` | Obtiene canciones de un album por ID. |

### Usuario

| Comando | Uso | Descripcion |
| --- | --- | --- |
| `status` | `status` | Muestra el usuario conectado. |
| `playlist-all` | `playlist-all` | Lista playlists del usuario autenticado. |
| `top-tracks` | `top-tracks` | Muestra tracks mas escuchados del usuario. |
| `top-artists` | `top-artists` | Muestra artistas mas escuchados del usuario. |
| `my-tracks` | `my-tracks` | Muestra tracks guardados en la biblioteca. |

### Reproductor

| Comando | Uso | Descripcion |
| --- | --- | --- |
| `player-state` | `player-state` | Muestra el estado actual del reproductor. |
| `devices` | `devices` | Lista dispositivos disponibles. |
| `play-device` | `play-device <device_id> <spotify_uri>` | Inicia reproduccion en un dispositivo especifico. |
| `transfer-playback` | `transfer-playback <device_id> [true\|false]` | Transfiere la reproduccion a otro dispositivo. |
| `current-track` | `current-track` | Muestra la cancion actual. |
| `pause` | `pause [device_id]` | Pausa la reproduccion. |
| `next-track` | `next-track [device_id]` | Salta a la siguiente cancion. |
| `previous-track` | `previous-track [device_id]` | Vuelve a la cancion anterior. |
| `volume` | `volume <0-100> [device_id]` | Cambia el volumen. |
| `shuffle` | `shuffle <on\|off> [device_id]` | Activa o desactiva modo aleatorio. |
| `recently-played` | `recently-played` | Muestra canciones reproducidas recientemente. |
| `queue` | `queue` | Muestra la cola de reproduccion. |
| `add-queue` | `add-queue <spotify_uri> [device_id]` | Agrega una cancion o episodio a la cola. |

## Ejemplos

Buscar un artista:

```bash
info No Te Va Gustar
```

Listar albums:

```bash
albums No Te Va Gustar
```

Listar canciones de un album:

```bash
tracks 0SrIBMYh2Vu2vSccAtLr6n
```

Ver dispositivos disponibles:

```bash
devices
```

Reproducir un track en un dispositivo:

```bash
play-device 64150b1037a4e4783c2e6376e5a2201ba2bf104b spotify:track:2cA8squ6qQvh5ioDHZVuwS
```

Cambiar volumen:

```bash
volume 50
```

Agregar un track a la cola:

```bash
add-queue spotify:track:2cA8squ6qQvh5ioDHZVuwS
```

## Notas

- Para los comandos del reproductor puede ser necesario tener Spotify abierto en algun dispositivo.
- Algunas acciones del reproductor requieren Spotify Premium.
- Si cambias los scopes del `.env`, volve a ejecutar `login`.


## Proximas mejoras

- Registrar auditorias de comandos ejecutados.
- Registrar auditorias de busquedas realizadas.
- Consultar historiales desde la CLI.
- Mejorar validaciones y mensajes de error.
