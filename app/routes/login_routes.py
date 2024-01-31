from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.Persona import Persona
from flask_bcrypt import Bcrypt
from app import db

# bp = bp_autenticacion_crear
bp = Blueprint('bp_login', __name__)

@bp.route('/login') 
def login():
  
    return render_template('login.html')



@bp.route('/login/autenticacion', methods=['GET', 'POST']) 
def autenticacion():

    correoUsuario = request.form['emailDocumento'].strip()
    contrasena = request.form['contrasena'].strip()
    bcrypt = Bcrypt()
    
    
    if correoUsuario != "" and contrasena != "" and len(correoUsuario) <= 255  and  6 <= len(contrasena) <= 15 and "@" in correoUsuario:  
        # es un correo
        consulta  = Persona.query.filter_by(correoPersona=correoUsuario).first()
        if consulta is not None: 
            contrasenaBD = consulta.contrasenaPersona
            
            if bcrypt.check_password_hash(contrasenaBD, contrasena):
                datosPersona = {
                    
                    'idUsuario' : consulta.idPersona,
                    'nombreUsuario': consulta.nombrePersona,
                    'apellidoUsuario': consulta.apellidoPersona,
                    'documentoUsuario':consulta.identificacionPersona,
                    'correoUsuario': consulta.correoPersona ,
                    'telefonoUsuario' : consulta.telefonoPersona, 
                    'idRol' : consulta.idRol, 
                }
                session['infoUsuario'] = datosPersona
                session['nombreUsuario'] = consulta.nombrePersona
                session['apellidoUsuario'] = consulta.apellidoPersona

                return redirect(url_for('bp_inicio.index'))
                   
    flash("datos invalidos", 'invalidados') 
    
    return render_template('login.html') 
