from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambia esto por algo seguro

    # Registro de blueprints
    from app.routes.auth import auth_bp
    from app.routes.files import files_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)

    return app
