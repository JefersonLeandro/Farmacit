from flask import Blueprint, render_template, request, session ,jsonify, redirect, url_for, flash 
from flask_login import  current_user , login_required
from app.models import Persona
from app import db
from .crear_cuenta_routes import generarCodigo, enviarCorreo
from flask import current_app
import time
import threading

bp = Blueprint('bp_verificacionCorreo', __name__)

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

            # borrar todos los datos de la sesion incluyendo codigo y de mas. IMPORTANTE
            respuesta = {'estado':'ok'} 
        except:
            db.session.rollback() 
            respuesta = {'estado':'fallo'} 
 
    else:
        respuesta = {'estado':'falloVerificacion'}  
     
    return jsonify(respuesta) 


@bp.route('/login/crear_cuenta/reenviar_codigo', methods=['POST', 'GET'])
def reenviarCorreo():
    try:
        tiempoActual = time.time()
        ultimoIntento = session.get("ultimoIntento")

        if "nIntentos" not in session:
            session["nIntentos"] = 5

        if ultimoIntento is None or (tiempoActual - ultimoIntento) >= 6:
            nIntentos = session.get("nIntentos")
            datos = session.get('datos_usuario')
            nombre = datos.get("nombre")
            correo = datos.get("correo")

            codigo = generarCodigo()
            session['codigo'] = codigo 

            if nIntentos > 0:
                enviarCorreo(nombre, correo, codigo)
                session["nIntentos"] = nIntentos - 1
                session["ultimoIntento"] = time.time()
                session.modified = True
            else:
                session["validacion"] = True
            return jsonify({'estado': 'ok', 'nIntentos': nIntentos})
        else:
            
            tiempoEspera = 60 -  (tiempoActual - ultimoIntento)
            return jsonify({'estado': 'espera', 'tiempo_restante': tiempoEspera})
            
    except Exception as e:
        return jsonify({'estado': 'Fallo', 'error': str(e)})

@bp.route('/login/crear_cuenta/reiniciar_estado', methods=['POST'])
def reiniciarEstado():

    try:
        correo = session.get('datos_usuario').get("correo")
        ultimoIntento = session.get("ultimoIntento", 0)
        validacion = session.get("validacion", False)
        tiempoActual = time.time()

        if ((tiempoActual - ultimoIntento) >= 170) and validacion and correo != None: 
           
            session["EnviarCorreo"][f"{correo}"]=True
            session["nIntentos"] = 3
            session["ultimoIntento"] = time.time()
            validacion = False
            session.modified = True
        
        return '', 204 # no contiene contenido pero salio exitoso la solicitud
    
    except Exception as e:
        return jsonify({'estado': 'Fallo', 'error': str(e)})
# tareas
# -  borrar variables de session cuando salga exitoso todo
# - poner procteccion de rutas. 
# - enviar el correo cuando termine los dos minutos con 50 segundos. 