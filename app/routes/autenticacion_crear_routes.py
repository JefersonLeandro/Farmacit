from flask import Blueprint, render_template, request, redirect, url_for
from app import db

bp = Blueprint('bp_autenticacion_crear', __name__)


@bp.route('/registro')
def registro():
    return render_template('registro.html')

@bp.route('/registro/crear_cuenta')
def crearCuenta():
    return render_template('crear_cuenta.html')


@bp.route('/registro/crear_cuenta/Registrar', methods=['GET', 'POST'])
def RegistrarUsuario():
    
 if request.method == 'POST':
     
    nombre = request.form['fNombrePersona']
    apellido = request.form['fApellidoPersona']
    identificacion = request.form['fIdentificacionPersona']
    correo = request.form['fCorreoPersona']
    telefono = request.form['fTelefonoPersona']
    contrasena = request.form['fContrasenaPersona']
    confirmarContrasena = request.form['fConfirmarContrasena']
    
     
    print(f" nombre : {nombre} , apellido : {apellido} , identificacion : {identificacion} , correo : {correo},telefono : {telefono} , contrasena: {contrasena}, confirmarContrasena : {confirmarContrasena}")
    

    return f"dentre a la funcion---{nombre}-{apellido}-{identificacion}-{correo}- {contrasena}-{confirmarContrasena}"
    
    




