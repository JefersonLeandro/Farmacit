from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.Persona import Persona
from flask_bcrypt import Bcrypt
from .index_routes import index
from app import db


#funciones



# bp = bp_autenticacion_crear
bp = Blueprint('bp_login', __name__)

@bp.route('/login') 
def login():
    vistaIndex = index()
    
    if current_user.is_authenticated:
        return vistaIndex
    return render_template('/autenticacion/login.html')

@bp.route('/login/autenticacion', methods=['GET', 'POST']) 
def autenticacion():
    if request.method == 'POST':
        correoUsuario = request.form['emailDocumento'].strip()
        contrasena = request.form['contrasena'].strip()
        bcrypt = Bcrypt()
        
        
        if correoUsuario != "" and contrasena != "" and len(correoUsuario) <= 255  and  6 <= len(contrasena) <= 15 and "@" in correoUsuario:  
            # es un correo
            consulta  = Persona.query.filter_by(correoPersona=correoUsuario).first()
            if consulta is not None: 
                contrasenaBD = consulta.contrasenaPersona
                
                if bcrypt.check_password_hash(contrasenaBD, contrasena):
                    login_user(consulta)#se marca como autenticado y recibe un objecto En este caso la persona
                    
                    return redirect(url_for('bp_inicio.index'))

        mensajeInvalidado = "datos invalidos" 
        flash(mensajeInvalidado, 'invalidados') 
      
    if current_user.is_authenticated:
        vistaIndex = index()
        return vistaIndex  
    return render_template('/autenticacion/login.html') 
    
@bp.route('/logout', methods=['GET']) 
def logout():
    logout_user()
    vistaIndex = index()
    
    return vistaIndex   



# datosPersona = {
                
            #     'idUsuario' : consulta.idPersona,
            #     'nombreUsuario': consulta.nombrePersona,
            #     'apellidoUsuario': consulta.apellidoPersona,
            #     'documentoUsuario':consulta.identificacionPersona,
            #     'correoUsuario': consulta.correoPersona ,
            #     'telefonoUsuario' : consulta.telefonoPersona, 
            #     'idRol' : consulta.idRol, 
            # }
            # # session['infoUsuario'] = datosPersona
            # # session['nombreUsuario'] = consulta.nombrePersona
            # # session['apellidoUsuario'] = consulta.apellidoPersona