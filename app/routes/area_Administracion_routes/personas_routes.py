from flask import Blueprint, render_template, request , redirect, url_for
from app.models import Persona , Rol
from flask_bcrypt import Bcrypt
from app import db

bp = Blueprint('bp_personas', __name__)

@bp.route('/area_administracion/personas' , methods=['POST', 'GET'])
def index():
    # listar
    roles  = Rol.query.all()
    personas = Persona.query.all()
    return render_template('/areaAdministracion/personas.html' , personas=personas , roles=roles)
    
    

@bp.route('/area_administracion/personas/acciones', methods=['POST'])
def acciones():
    
    if request.method == 'POST':
        
        idPersona = request.form['fIdPersona']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
          insertar()
        elif accion == "Modificar":
          modificar(idPersona)
     
        elif accion == "Eliminar":
         eliminar(idPersona)    
         
   
    return redirect(url_for('bp_personas.index'))
    
 
def insertar():
    
    bcrypt = Bcrypt()
    
    nombrePersona = request.form['fNombrePersona']
    apellidoPersona = request.form['fApellidoPersona'] 
    identificacionPersona = request.form['fIdentificacionPersona'] 
    correoPersona =  request.form['fCorreoPersona']
    telefonoPersona =  request.form['fTelefonoPersona']
    contrasenaPersona =  request.form['fContrasenaPersona']
    idRol =request.form['fIdRol'] 
    
    hashedContrasena = bcrypt.generate_password_hash(contrasenaPersona).decode('utf-8')
    nuevaPersona = Persona(idPersona= None, nombrePersona=nombrePersona, apellidoPersona = apellidoPersona, identificacionPersona = identificacionPersona, correoPersona = correoPersona, telefonoPersona = telefonoPersona, contrasenaPersona = hashedContrasena , idRol = idRol)
    db.session.add(nuevaPersona)
    db.session.commit()
   
def modificar(idPersona):
    
    persona = Persona.query.get_or_404(idPersona)
    
    persona.nombrePersona = request.form['fNombrePersona']
    persona.apellidoPersona = request.form['fApellidoPersona'] 
    persona.identificacionPersona = request.form['fIdentificacionPersona']  
    persona.telefonoPersona =  request.form['fTelefonoPersona']
    persona.idRol=request.form['fIdRol'] 
   
    db.session.commit()
    
   

def eliminar(idPersona):
    
    persona = Persona.query.get_or_404(idPersona)
    db.session.delete(persona)
    db.session.commit()
    


