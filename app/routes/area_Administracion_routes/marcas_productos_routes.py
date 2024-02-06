from flask import Blueprint, render_template , request , redirect , url_for , flash
from sqlalchemy.exc import IntegrityError
from app.models import MarcaProducto
from flask_login import current_user
from app import db

bp = Blueprint('bp_marcas_productos', __name__)


@bp.route('/area_administracion/productos/marcas_productos' , methods=['POST', 'GET'])
def index():
    # listar
    if current_user.is_authenticated and current_user.idRol == 3:    
      marcasProductos = MarcaProducto.query.all()
      return render_template('/areaAdministracion/marcas_productos.html' , marcasProductos = marcasProductos)
    return redirect(url_for('bp_inicio.index'))

@bp.route('/area_administracion/productos/marcas_productos/acciones', methods=['POST' , 'GET'])
def acciones():
    if current_user.is_authenticated and current_user.idRol == 3 and request.method == 'POST': 
      
      idMarcaProducto = request.form['fIdMarcaProducto']
      accion = request.form['fAccion']
      
      if accion == "Ingresar":       
        insertar()
      
      elif accion == "Modificar":
        modificar(idMarcaProducto)
      
      elif accion == "Eliminar":
        eliminar(idMarcaProducto)    
          
      return redirect(url_for('bp_marcas_productos.index'))
    return redirect(url_for('bp_inicio.index'))



def insertar():
    
    nombreMarca =request.form['fNombreMarca'] 
  
    nuevaMarca = MarcaProducto(idMarcaProducto= None, nombreMarca=nombreMarca)
    db.session.add(nuevaMarca)
    db.session.commit()
   
def modificar(idMarcaProducto):
    
    marcaProducto = MarcaProducto.query.get_or_404(idMarcaProducto)
    marcaProducto.nombreMarca = request.form['fNombreMarca']
    db.session.commit()

def eliminar(idMarcaProducto):
    
    try:
      marcaProducto = MarcaProducto.query.get_or_404(idMarcaProducto)
      db.session.delete(marcaProducto)
      db.session.commit()
    except IntegrityError as e:
      db.session.rollback()  # Deshace la transacción para evitar cambios no deseados
      flash('Error de integridad referencial. No se puede eliminar el producto debido a relaciones existentes.', 'errorIntegridad')