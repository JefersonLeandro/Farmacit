from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.Persona import Persona
from flask_bcrypt import Bcrypt
from app import db



bp = Blueprint('bp_login', __name__)

@bp.route('/login') 
def login():
  
    if current_user.is_authenticated:
         return redirect(url_for('bp_inicio.index'))
    return render_template('/autenticacion/login.html')

@bp.route('/login/autenticacion', methods=['POST','GET']) 
def autenticacion():
    if not current_user.is_authenticated:
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
                        login_user(consulta)#se marca como autenticado y recibe un objecto en este caso la persona
                        return redirect(url_for('bp_inicio.index'))

            mensajeInvalidado = "datos invalidos" 
            flash(mensajeInvalidado, 'invalidados')  
        return render_template('/autenticacion/login.html') 
    return redirect(url_for('bp_inicio.index'))
    
@bp.route('/logout', methods=['GET']) 
def logout():
    if current_user.is_authenticated:
        logout_user()
        paginaAnterior = request.referrer
        return redirect(paginaAnterior)
    return redirect(url_for('bp_inicio.index'))