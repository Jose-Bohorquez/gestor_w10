from flask import Blueprint

files_bp = Blueprint('files', __name__)

@files_bp.route('/files')
def files_home():
    return "¡Página de gestión de archivos!"
