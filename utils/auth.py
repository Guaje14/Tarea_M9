# Importa UserMixin para gestionar usuarios con Flask-Login
from flask_login import UserMixin

# Importa las credenciales válidas desde la configuración
from config import VALID_USERNAME, VALID_PASSWORD


# Clase de usuario para la autenticación
class User(UserMixin):
    def __init__(self, username: str):
        # Guarda el nombre de usuario como id
        self.id = username


# Función que valida si las credenciales introducidas son correctas
def validate_user(username: str, password: str) -> bool:
    return username == VALID_USERNAME and password == VALID_PASSWORD