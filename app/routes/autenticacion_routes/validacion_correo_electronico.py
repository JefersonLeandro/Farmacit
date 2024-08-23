from flask import Blueprint, render_template, request , redirect, url_for 
from flask_login import  current_user , login_required
from app.models import Farmacia
from app import db

bp = Blueprint('bp_verificacionCorreo', __name__)

@bp.route('/login/crear_cuenta/verificacion_correo' , methods=['POST', 'GET'])

def index():
    #verificacion
    # hashedContrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    # nuevaPersona = Persona(nombrePersona=nombre, apellidoPersona = apellido, identificacionPersona = identificacion, correoPersona = correo, telefonoPersona = telefono, contrasenaPersona = hashedContrasena, idRol= 1)
    # db.session.add(nuevaPersona)
    # db.session.commit()
    # mensajeExito = "Registro Exitoso"
    # flash(mensajeExito, 'exito')

    # return redirect(url_for('bp_login.login'))
    

    return render_template('/areaAdministracion/farmacias.html')
    return redirect(url_for('bp_inicio.index'))
    
