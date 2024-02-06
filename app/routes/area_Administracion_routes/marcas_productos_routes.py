from flask import Blueprint, render_template , request , redirect , url_for
from app.models import MarcaProducto
from app import db

bp = Blueprint('bp_marcas_productos', __name__)


@bp.route('/area_administracion/productos/marcas_productos' , methods=['POST', 'GET'])
def index():
    # listar
    marcasProductos = MarcaProducto.query.all()
    return render_template('/areaAdministracion/marcas_productos.html' , marcasProductos = marcasProductos)

@bp.route('/area_administracion/productos/marcas_productos/acciones', methods=['POST'])
def acciones():
    
    if request.method == 'POST':
        
        idMarcaProducto = request.form['fIdMarcaProducto']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
          insertar()
         
        elif accion == "Modificar":
          modificar(idMarcaProducto)
         
        elif accion == "Eliminar":
          eliminar(idMarcaProducto)    
         
    return redirect(url_for('bp_marcas_productos.index'))



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
  
    marcaProducto = MarcaProducto.query.get_or_404(idMarcaProducto)
    db.session.delete(marcaProducto)
    db.session.commit()