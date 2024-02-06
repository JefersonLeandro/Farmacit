from flask import Blueprint, render_template, request , redirect, url_for , flash 
from app.models import Producto , MarcaProducto
from sqlalchemy.exc import IntegrityError
from app import db

bp = Blueprint('bp_productos', __name__)

@bp.route('/area_administracion/productos' , methods=['POST', 'GET'])
def index():
    # listar
    productos = Producto.query.all()
    marcasProductos = MarcaProducto.query.all()
    return render_template('/areaAdministracion/productos.html' , productos = productos , marcasProductos = marcasProductos)

@bp.route('/area_administracion/productos/acciones', methods=['POST'])
def acciones():
    
    if request.method == 'POST':
        
        idProducto = request.form['fIdProducto']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
          insertar()
          
        elif accion == "Modificar":
          modificar(idProducto)
     
        elif accion == "Eliminar":
          eliminar(idProducto)    
         
   
    return redirect(url_for('bp_productos.index'))
    
 
def insertar():
    
    nombreProducto = request.form['fNombreProducto']
    descripcionUnidad = request.form['fDescripcionUnidad'] 
    descripcionProductoGeneral = request.form['fDescripcionProductoGeneral'] 
    stockProducto =  request.form['fStockProducto']
    precioProducto =  request.form['fPrecioProducto']
    idMarcaProducto =  request.form['fIdMarcaProducto']
   

    nuevoProducto = Producto(idProducto= None, nombreProducto=nombreProducto, descripcionUnidad = descripcionUnidad, descripcionProductoGeneral = descripcionProductoGeneral, stockProducto = stockProducto, precioProducto = precioProducto, idMarcaProducto = idMarcaProducto)
    db.session.add(nuevoProducto)
    db.session.commit()
    
def modificar(idProducto):

    producto = Producto.query.get_or_404(idProducto)
    
    producto.nombreProducto = request.form['fNombreProducto']
    producto.descripcionUnidad = request.form['fDescripcionUnidad'] 
    producto.descripcionProductoGeneral =  request.form['fDescripcionProductoGeneral'] 
    producto.stockProducto =  request.form['fStockProducto']
    producto.precioProducto =  request.form['fPrecioProducto']
    producto.idMarcaProducto = request.form['fIdMarcaProducto'] 

    db.session.commit()
    
def eliminar(idProducto):
    
 
  try:
    producto = Producto.query.get_or_404(idProducto)
    db.session.delete(producto)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()  # Deshace la transacción para evitar cambios no deseados
    flash('Error de integridad referencial. No se puede eliminar el producto debido a relaciones existentes.', 'errorIntegridad')
    
   
    