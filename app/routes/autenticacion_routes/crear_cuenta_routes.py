from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash , session
from wtforms import Form, StringField, PasswordField, validators
from app.models.Persona import Persona
from flask_login import  current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
import random 
from flask_mail import Message

bp = Blueprint('bp_crear_cuenta', __name__)



@bp.route('/login/crear_cuenta')
def crearCuenta():
    if current_user.is_authenticated:
        
        return redirect(url_for('bp_inicio.index'))
    return render_template('autenticacion/crear_cuenta.html') 

class RegistrationForm(Form):
    
    fNombrePersona = StringField('fNombrePersona', [
        validators.DataRequired(message="Nombre requerido."),
        validators.Length(min=4, max=28, message="Ingrese un nombre valido.")
        ])
    
    fApellidoPersona = StringField('fApellidoPersona', [
        validators.DataRequired(message="Apellido requerido."),
        validators.Length(min=4, max=28, message="Ingrese un Apellido valido.")
        ])
    
    fIdentificacionPersona = StringField('fIdentificacionPersona', [
        validators.DataRequired(message="Identificación requerida."),
        validators.Length(min= 6, max=12, message="Ingrese una identificacion valida.")
        ])
    fTelefonoPersona = StringField('fTelefonoPersona', [
        validators.DataRequired(message="Telefono requerido."),
        validators.Length(min= 10, max=12, message="Ingrese un telefono valido.")
        ])
    
    fCorreoPersona = StringField('fCorreoPersona', [
        validators.DataRequired(message="Correo Electronico requerido."),
        validators.Email(message="Ingrese una dirección de correo electrónico válida."),
        validators.Length(max=255, message="El correo execede el numero maximo de caracteres.")
        ])
    
    fContrasenaPersona = PasswordField('fContrasenaPersona', validators=[
        validators.DataRequired(message="La contraseña es requerida."),
        validators.Length(min=6, max=15, message="Ingrese una contraseña de 6 a 15 caracteres.")
    ])
    
    fConfirmarContrasena = PasswordField('fConfirmarContrasena', validators=[
        validators.EqualTo('fContrasenaPersona', message='Las contraseñas deben coincidir.')
    ])
    
@bp.route('/login/crear_cuenta/Registrar', methods=['GET', 'POST'])
def RegistrarUsuario():
    
    if request.method == 'POST':
        nombre = request.form['fNombrePersona']
        apellido = request.form['fApellidoPersona']
        identificacion = request.form['fIdentificacionPersona']
        correo = request.form['fCorreoPersona'].strip()
        telefono = request.form['fTelefonoPersona']
        contrasena = request.form['fContrasenaPersona'].strip()
        bcrypt = Bcrypt()

        
        # Verificar si el correo ya está en la base de datos
        verificar = Persona.query.filter_by(correoPersona=correo).first()
        form = RegistrationForm(request.form) 
        
        if not ('fCorreoPersona' in form.errors) and verificar:
           
            # el correo ya esta registrado
            flash("El correo suministrado ya se encuentra registrado", 'error')
    
            return render_template('/autenticacion/crear_cuenta.html' , form=form)
        
        elif  form.validate():

            hashedContrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
            
            codigo = generarCodigo()
            
            session['codigo'] = codigo  
            session['datos_usuario'] = {
                "nombre" : nombre,
                "apellido" : apellido,
                "identificacion" : identificacion, 
                "correo" : correo,
                "telefono" : telefono,
                "contrasena" : hashedContrasena
            } 

            verificacionCorreo(nombre, correo,codigo, form)
            
                   
            return render_template('/autenticacion/validacion_correo_electronico.html', correo = correo) 
        else:
            return render_template('/autenticacion/crear_cuenta.html' , form=form)
   
    if current_user.is_authenticated:
        return redirect(url_for('bp_inicio.index'))
    return render_template("/autenticacion/crear_cuenta.html")


def verificacionCorreo(nombre, correo, codigo, form ):

    if "EnviarCorreo" not in session:
        session["EnviarCorreo"] = {}

    bandera = session.get("EnviarCorreo").get(f"{correo}", True)
    
    if (bandera):
        try:  
            enviarCorreo(nombre,correo,codigo)
            session["EnviarCorreo"][f"{correo}"]=False

        except Exception :
            render_template('/autenticacion/crear_cuenta.html' , form=form)

def enviarCorreo(nombre,correo,codigo):
    from app import mail

    msg = Message(
    subject="Codigo de verificación (Farmacit)",
    sender="Farmacit.envio.correos@gmail.com",
    recipients=[f"{correo}"],
    html=f"""
    <html>
        <body>
            <header>
                <span>Hola {nombre}</span>
            </header>
            <p>Estamos a un solo paso de terminar.</p>
            <p>Este es el codigo de verificación <strong>{codigo}</strong>. ¡Gracias por su paciencia!</p> 
            <a href="#">Escribelo aqui.</a>
            <hr>
            <strong>Importante</strong>
            <p>No compartas tu codigo</p>
            <footer>
                <p>Conctátanos</p>
                <p>farmacit.servicio.cliente@gmail.com</p>
                <div style='display:flex;, gap:15px;  '>
                    <a href='www.facebook.com' >Facebook</a>
                    <a href='www.x.com' >Twitter</a>
                    <a href='www.Instagram.com' >Instagram</a>
                </div>
            </footer>
        </body>
    </html>
    """
    )

    mail.send(msg) 

def generarCodigo():
    codigo = random.randint(1000, 9999)
    return codigo 
