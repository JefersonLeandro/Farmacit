from flask import Blueprint, render_template, request, session ,jsonify, redirect, url_for, flash 
from app.models import Persona
from flask_login import  current_user
from app import db
from .crear_cuenta_routes import generarCodigo, enviarCorreo
import time


bp = Blueprint('bp_verificacionCorreo', __name__)

@bp.route('/login/crear_cuenta/verificacion_correo' , methods=['POST', 'GET'])
def index():

    if not current_user.is_authenticated and "datos_usuario" in session:
        if request.method=="POST":

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
                        idRol=1)
                    
                    db.session.add(nuevaPersona)
                    db.session.commit()
                    session.clear()
                    respuesta = {'estado':'ok'}
                except:
                    db.session.rollback()
                    respuesta = {'estado':'fallo'}
            else:
                respuesta = {'estado':'falloVerificacion'}
            return jsonify(respuesta)
         
        return render_template("autenticacion/validacion_correo_electronico.html")
    return redirect(url_for('bp_inicio.index'))

@bp.route('/login/crear_cuenta/reenviar_codigo', methods=['POST', 'GET'])
def reenviarCorreo():
    if not current_user.is_authenticated and "datos_usuario" in session:
        # agregar un token verificacion para que por defecto no muestre informacion de la respuesta json. 
        try:
            tiempoActual = time.time()
            ultimoIntento = session.get("ultimoIntento")

            if "nIntentos" not in session:
                session["nIntentos"] = 5

            if ultimoIntento is None or (tiempoActual - ultimoIntento) >= 58:
                nIntentos = session.get("nIntentos")
                datos = session.get('datos_usuario')
                nombre = datos.get("nombre")
                correo = datos.get("correo")

                codigo = generarCodigo()
                session['codigo'] =codigo

                if nIntentos > 0:
                    enviarCorreo(nombre, correo, codigo)
                    session["nIntentos"] = nIntentos - 1
                    session["ultimoIntento"] =time.time()
                    session.modified = True
                else:
                    session["validacion"] =True
                return jsonify({'estado': 'ok', 'nIntentos': nIntentos})
            else:
                tiempoEspera = 58 -  (tiempoActual - ultimoIntento)
                return jsonify({'estado': 'espera', 'tiempo_restante': tiempoEspera})     
        except Exception as e:
            return jsonify({'estado': 'Fallo', 'error': str(e)})
    return redirect(url_for('bp_inicio.index'))


@bp.route('/login/crear_cuenta/reiniciar_estado', methods=['POST', 'GET'])
def reiniciarEstado():
    if not current_user.is_authenticated and "datos_usuario" in session:
        if request.method=="POST":
            try:
                nombre = session.get('datos_usuario').get("nombre")
                correo = session.get('datos_usuario').get("correo")
            
                ultimoIntento = session.get("ultimoIntento", 0)
                validacion = session.get("validacion", False)
                tiempoActual = time.time()
            
                if ((tiempoActual - ultimoIntento) >= 170) and validacion and correo != None:
                
                    session["EnviarCorreo"][f"{correo}"]=True
                    session["nIntentos"] = 3
                    session["ultimoIntento"] = time.time()
                    session["validacion"] = False
                    codigo = generarCodigo()
                    session['codigo'] =codigo
                    session.modified = True
                    enviarCorreo(nombre, correo, codigo)

                return '', 204 # no contiene contenido pero salio exitoso la solicitud
            
            except Exception as e:
                return jsonify({'estado': 'Fallo', 'error': str(e)})
            
        return render_template("autenticacion/validacion_correo_electronico.html")
    return redirect(url_for('bp_inicio.index'))
# tareas
# - 
