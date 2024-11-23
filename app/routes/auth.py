from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils import validate_user, register_user

auth_bp = Blueprint('auth', __name__)

# Ruta para la página de inicio
@auth_bp.route('/')
def home():
    return render_template('home.html')  # Renderiza la página de inicio

# Ruta para la página de inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contraseña']
        
        # Validamos usuario con los datos en el archivo Excel
        if validate_user(username, password):
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('auth.home'))  # Redirigir al inicio
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')  # Formulario de inicio de sesión

# Ruta para la página de registro de usuarios
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Capturamos los datos del formulario
            data = {
                'tipo_de_documento': request.form['tipo_de_documento'],
                'nuip': request.form['nuip'],
                'nombres': request.form['nombres'],
                'apellidos': request.form['apellidos'],
                'fecha_nacimiento': request.form['fecha_nacimiento'],
                'correo': request.form['correo'],
                'usuario': request.form['usuario'],
                'contraseña': request.form['contraseña'],
                'telefono': request.form['telefono'],
            }

            # Registramos el usuario en el archivo Excel
            register_user(data)
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('auth.login'))  # Redirigir al login
        except Exception as e:
            flash(str(e), 'danger')  # Mostramos el error en la interfaz

    return render_template('register.html')  # Formulario de registro
