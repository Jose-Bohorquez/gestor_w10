# Aquí se colocarán funciones de utilidad para el proyecto
import pandas as pd
import openpyxl
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

def register_user(data):
    # Ruta al archivo Excel
    excel_path = 'users.xlsx'

    try:
        # Abre el archivo Excel o crea uno nuevo si no existe
        try:
            workbook = openpyxl.load_workbook(excel_path)
            sheet = workbook.active
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Escribe los encabezados
            sheet.append([
                'Tipo de Documento', 'NUIP', 'Nombres', 'Apellidos',
                'Fecha de Nacimiento', 'Correo Electrónico', 'Usuario',
                'Contraseña', 'Teléfono', 'Fecha y Hora de Registro'
            ])

        # Agrega los datos del usuario
        sheet.append([
            data['tipo_de_documento'],
            data['nuip'],
            data['nombres'],
            data['apellidos'],
            data['fecha_nacimiento'],
            data['correo'],
            data['usuario'],
            data['contraseña'],  # En producción, encripta esta información
            data['telefono'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
        ])

        # Guarda el archivo Excel
        workbook.save(excel_path)
    except Exception as e:
        raise Exception(f"Error al registrar usuario: {e}")
