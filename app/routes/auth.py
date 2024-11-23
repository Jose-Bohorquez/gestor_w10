from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.utils import validate_user, register_user, get_users, get_user_role, role_required, update_user, toggle_user_status  # Importar las funciones necesarias

auth_bp = Blueprint('auth', __name__)

# Ruta para ver todos los usuarios (solo superadmin o admin)
@auth_bp.route('/admin', methods=['GET'])
@role_required(['superadmin', 'admin'])  # Ahora está correctamente importado
def admin_panel():
    if 'usuario' not in session or session['rol'] not in ['superadmin', 'admin']:
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    users = get_users()  # Obtener todos los usuarios
    return render_template('admin.html', users=users)  # Mostrar los usuarios en la vista de admin


# Ruta para la página de inicio
@auth_bp.route('/')
def home():
    usuario = session.get('usuario', None)
    return render_template('home.html', usuario=usuario)  # Renderiza la página de inicio

# Ruta para la página de inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contraseña']

        # Validamos usuario con los datos en el archivo Excel
        if validate_user(username, password):
            # Obtener el rol del usuario
            user_role = get_user_role(username)

            if user_role:
                # Guardar usuario y rol en sesión
                session['usuario'] = username
                session['rol'] = user_role  # Guardamos el rol en la sesión
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('auth.dashboard'))  # Redirigir al dashboard
            else:
                flash('Rol no encontrado para el usuario', 'danger')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')  # Formulario de inicio de sesión

# Ruta para la página de registro de usuarios
@auth_bp.route('/register', methods=['GET', 'POST'])
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
                'rol': 'user',  # Asignar por defecto el rol de "user"
                'estado_usuario': 'activo'  # Asignar estado_usuario como 'activo' por defecto
            }

            # Si el usuario es un admin, supervisor o superadmin, asignamos ese rol
            if data['usuario'] == 'admin':
                data['rol'] = 'admin'
            elif data['usuario'] == 'superadmin':
                data['rol'] = 'superadmin'

            # Registramos el usuario en el archivo Excel
            register_user(data)
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('auth.login'))  # Redirigir al login
        except Exception as e:
            flash(str(e), 'danger')  # Mostramos el error en la interfaz

    return render_template('register.html')  # Formulario de registro


# Ruta para el dashboard (después de iniciar sesión)
@auth_bp.route('/dashboard')
@role_required(['admin', 'superadmin', 'supervisor'])  # Supervisores también pueden acceder
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    flash('Debes iniciar sesión para acceder al dashboard.', 'warning')
    return redirect(url_for('auth.login'))  # Redirigir al login si no hay sesión

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('rol', None)  # Eliminar también el rol
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('auth.login'))  # Redirigir al login

# Ruta para cambiar el estado de un usuario
@auth_bp.route('/admin/user/toggle_status/<int:user_id>', methods=['POST'])
@role_required(['superadmin', 'admin'])  # Solo los administradores o superadministradores pueden cambiar el estado
def toggle_user_status_route(user_id):
    if 'usuario' not in session or session['rol'] not in ['superadmin', 'admin']:
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    new_status = request.form.get('estado_usuario')
    try:
        toggle_user_status(user_id, new_status)  # Actualiza el estado
        flash('Estado del usuario actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar el estado del usuario: {str(e)}', 'danger')

    return redirect(url_for('auth.admin_panel'))  # Redirigir al panel de administración
