from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, PasswordField, validators
from app.models.Persona import Persona
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm 
from app import db



app = Flask(__name__)
bp = Blueprint('bp_autenticacion_crear', __name__)


@bp.route('/login') 
def login():
    return render_template('login.html')

@bp.route('/login/crear_cuenta')
def crearCuenta():
    return render_template('crear_cuenta.html') 



class RegistrationForm(Form):
    
    fNombrePersona = StringField('fNombrePersona', [
        validators.DataRequired(message="Nombre requerido"),
        validators.Length(min=4, max=28, message="Ingrese un nombre valido")
        ])
    
    fApellidoPersona = StringField('fApellidoPersona', [
        validators.DataRequired(message="Apellido requerido"),
        validators.Length(min=4, max=28, message="Ingrese un Apellido valido")
        ])
    
    fIdentificacionPersona = StringField('fIdentificacionPersona', [
        validators.DataRequired(message="Identificacion requerida"),
        validators.Length(min= 6, max=12, message="Ingrese una identificacion valida")
        ])
    fTelefonoPersona = StringField('fTelefonoPersona', [
        validators.DataRequired(message="Telefono requerido"),
        validators.Length(min= 10, max=12, message="Ingrese un telefono valido")
        ])
    
    fCorreoPersona = StringField('fCorreoPersona', [
        validators.DataRequired(message="Correo Electronico requerido"),
        validators.Email(message="Ingrese una dirección de correo electrónico válida"),
        validators.Length(max=120, message="El correo execede el numero maximo de caracteres")
        ])
    
    fContrasenaPersona = PasswordField('fContrasenaPersona', validators=[
        validators.DataRequired(message="La contraseña es requerida"),
        validators.Length(min=6, max=15, message="Ingrese una contraseña de 6 a 15 caracteres")
    ])
    
    fConfirmarContrasena = PasswordField('fConfirmarContrasena', validators=[
        validators.EqualTo('fContrasenaPersona', message='Las contraseñas deben coincidir')
    ])
    
@bp.route('/login/crear_cuenta/Registrar', methods=['GET', 'POST'])
def RegistrarUsuario():
    
    if request.method == 'POST':
        nombre = request.form['fNombrePersona']
        apellido = request.form['fApellidoPersona']
        identificacion = request.form['fIdentificacionPersona']
        correo = request.form['fCorreoPersona']
        telefono = request.form['fTelefonoPersona']
        contrasena = request.form['fContrasenaPersona']
        bcrypt = Bcrypt()

        
        # Verificar si el correo ya está en la base de datos
        verificar = Persona.query.filter_by(correoPersona=correo).first()
        form = RegistrationForm(request.form) 
    
    
        if  form.validate():
            if verificar: 
                # el correo ya esta registrado
                flash("El correo suministrado ya se encuentra registrado", 'error')
        
                return render_template('crear_cuenta.html' , form=form)
            
            hashedContrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
            nuevaPersona = Persona(nombrePersona=nombre, apellidoPersona = apellido, identificacionPersona = identificacion, correoPersona = correo, telefonoPersona = telefono, contrasenaPersona = hashedContrasena, idRol= 1)
            db.session.add(nuevaPersona)
            db.session.commit()
            flash("Registro Exitoso", 'exito')
            return redirect(url_for('bp_autenticacion_crear.login'))
        
        else:
            return render_template('crear_cuenta.html' , form=form)
    return render_template("crearCuenta_cuenta.html")

    
    
    




