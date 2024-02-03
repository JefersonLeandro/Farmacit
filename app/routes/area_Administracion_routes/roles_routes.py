from flask import Blueprint, render_template , request , redirect , url_for
from app.models import Rol
from app import db

bp = Blueprint('bp_roles', __name__)


@bp.route('/area_administracion/personas/roles' , methods=['POST', 'GET'])
def index():
    # listar
    roles = Rol.query.all()
    return render_template('/areaAdministracion/roles.html' , roles=roles)

@bp.route('/area_administracion/personas/roles/acciones', methods=['POST'])
def acciones():
    
    if request.method == 'POST':
        
        idRol = request.form['fIdRol']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
         insertar()
         
        elif accion == "Modificar":
         modificar(idRol)
         
        elif accion == "Eliminar":
         eliminar(idRol)    
         
    return redirect(url_for('bp_roles.index'))



def insertar():
    
    nombreRol =request.form['fNombreRol'] 
    nuevoRol = Rol(idRol= None, nombreRol=nombreRol)
    db.session.add(nuevoRol)
    db.session.commit()
   
def modificar(idRol):
    
    rol = Rol.query.get_or_404(idRol)
    rol.nombreRol = request.form['fNombreRol']
    db.session.commit()

def eliminar(idRol):
    
    rol = Rol.query.get_or_404(idRol)
    db.session.delete(rol)
    db.session.commit()