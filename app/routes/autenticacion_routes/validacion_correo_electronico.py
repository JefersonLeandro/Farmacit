from flask import Blueprint, render_template, request, session ,jsonify, redirect, url_for, flash 
from flask_login import  current_user , login_required
from app.models import Persona
from app import db
from .crear_cuenta_routes import generarCodigo, enviarCorreo

bp = Blueprint('bp_verificacionCorreo', __name__)

# cambiar por un un diccionario y dejar para cada usuario ya que se estaria dejando para todos
nIntentos = 10 

@bp.route('/login/crear_cuenta/verificacion_correo' , methods=['POST', 'GET'])

def index():
    #verificacion

    codigoEntrada = request.get_json()
    codigo = str(session.get('codigo'))   
  
    print("codigo es : ",codigo)
    print("codigoEntrada : ",codigoEntrada)
 
    if codigoEntrada.isdigit() and codigo == codigoEntrada:     

        datos = session.get('datos_usuario') 
         
        try:
            nuevaPersona = Persona(
                nombrePersona=datos.get("nombre"),
                apellidoPersona = datos.get("apellido"),
                identificacionPersona = datos.get("identificacion"),
                correoPersona = datos.get("correo"), 
                telefonoPersona = datos.get("telefono"),
                contrasenaPersona = datos.get("contrasena"),
                idRol= 1)
            
            db.session.add(nuevaPersona)
            db.session.commit()

            # borrar todos los datos de la sesion incluyendo codigo y de mas. 
            respuesta = {'estado':'ok'} 
        except:
            db.session.rollback() 
            respuesta = {'estado':'fallo'} 
 
    else:
        respuesta = {'estado':'falloVerificacion'}  
     
    return jsonify(respuesta) 


@bp.route('/login/crear_cuenta/reenviar_codigo' , methods=['POST', 'GET'])
def reenviarCorreo():
    
    global nIntentos
    nIntentos-=1

    datos = session.get('datos_usuario')
    nombre = datos.get("nombre")
    correo = datos.get("correo")

    codigo = generarCodigo()
    session['codigo'] = codigo 

    try:
        enviarCorreo(nombre, correo, codigo)
        respuesta = {'estado':'ok','nIntentos' : nIntentos} 
    except Exception as e:
        render_template('/autenticacion/validacion_correo_electronico.html', correo = correo)
        respuesta = {'estado':'Fallo'} 
    
    return jsonify(respuesta) 
    
    
