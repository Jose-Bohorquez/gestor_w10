# Aquí se colocarán funciones de utilidad para el proyecto
import pandas as pd
from datetime import datetime

def load_users(file_path='users.xlsx'):
    """Carga los usuarios desde un archivo Excel."""
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        raise Exception("Archivo de usuarios no encontrado.")

def validate_user(username, password, file_path='users.xlsx'):
    """Valida si el usuario y contraseña son correctos."""
    users = load_users(file_path)
    user = users[(users['usuario'] == username) & (users['contraseña'] == password)]
    return not user.empty


def register_user(data, file_path='users.xlsx'):
    """Registra un nuevo usuario en el archivo Excel."""
    users = load_users(file_path)

    # Validar que no exista un usuario con el mismo 'usuario' o 'nuip'
    if not users[(users['usuario'] == data['usuario']) | (users['nuip'] == data['nuip'])].empty:
        raise ValueError("El usuario o número de documento ya existe.")

    # Añadir fecha y hora de registro
    data['fecha_hora_registro'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Convertir a DataFrame y guardar
    new_user = pd.DataFrame([data])
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_excel(file_path, index=False)
