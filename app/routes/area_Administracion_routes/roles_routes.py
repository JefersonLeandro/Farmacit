from flask import Blueprint, render_template , request , redirect , url_for , flash
from sqlalchemy.exc import IntegrityError
from flask_login import current_user , login_required
from app.models import Rol
from app import db

bp = Blueprint('bp_roles', __name__)


@bp.route('/area_administracion/personas/roles' , methods=['POST', 'GET'])
@login_required
def index():
    # listar
    if current_user.is_authenticated and current_user.idRol == 3: 
        roles = Rol.query.all()
        return render_template('/areaAdministracion/roles.html' , roles=roles)
    return redirect(url_for('bp_inicio.index'))
        

@bp.route('/area_administracion/personas/roles/acciones', methods=['POST' , 'GET'])
@login_required
def acciones():
    
    if current_user.is_authenticated and current_user.idRol == 3 and request.method == 'POST': 
       
        idRol = request.form['fIdRol']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
            insertar()
        
        elif accion == "Modificar":
            modificar(idRol)
        
        elif accion == "Eliminar":
            eliminar(idRol)    
            
        return redirect(url_for('bp_roles.index'))
       
    return redirect(url_for('bp_inicio.index'))

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
    
    try:
        rol = Rol.query.get_or_404(idRol)
        db.session.delete(rol)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()  # Deshace la transacción para evitar cambios no deseados
        flash('Error de integridad referencial. No se puede eliminar el producto debido a relaciones existentes.', 'errorIntegridad')
    
   