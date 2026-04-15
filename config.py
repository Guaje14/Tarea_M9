# Importa Path para trabajar con rutas
from pathlib import Path


# Carpeta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpeta de assets
ASSETS_DIR = BASE_DIR / "assets"

# Carpeta de datos
DATA_DIR = BASE_DIR / "data"

# Carpeta de imágenes
IMG_DIR = ASSETS_DIR / "img"

# Carpeta de escudos
SHIELDS_DIR = ASSETS_DIR / "shields"


# Clave secreta de Flask
SECRET_KEY = "m9-dashboard-secret-key"

# Título de la aplicación
APP_TITLE = "Datathletics"


# Usuario válido para login
VALID_USERNAME = "admin"

# Contraseña válida para login
VALID_PASSWORD = "admin"


# Tiempo de caché en segundos
CACHE_TIMEOUT = 120


# Posibles nombres de la base de datos de estadísticas
STATS_DB_CANDIDATES = [
    DATA_DIR / "stats_players.db",
    DATA_DIR / "stats_players.sqlite",
    DATA_DIR / "stats_players",
]


# Posibles nombres de la base de datos GPS
GPS_DB_CANDIDATES = [
    DATA_DIR / "gps_players.db",
    DATA_DIR / "gps_players.sqlite",
    DATA_DIR / "gps_players",
]


# Posibles rutas del logo de la app
LOGO_CANDIDATES = [
    "/assets/img/Datathletics.png",
    "/assets/img/datathletics.png",
    "/assets/img/logo.png",
]