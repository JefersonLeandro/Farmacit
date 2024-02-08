from flask import Blueprint, render_template , redirect , url_for , request
from flask_login import current_user
from sqlalchemy.orm import aliased
from app.models.Imagen import Imagen 
from app.models.Producto import Producto 
from app.models.ProductoDeseado import ProductoDeseado
from app import db



bp = Blueprint('bp_favoritos', __name__)

@bp.route('/productos_deseados')
def index():
    
    if current_user.is_authenticated:
        # SELECT p.idProducto, p.nombreProducto, p.descripcionUnidad, p.descripcionProductoGeneral, p.precioProducto, d.idProductoD, i.nombreImagen , i.tipoImagen FROM productodeseado d JOIN producto p ON d.idProducto = p.idProducto JOIN imagen i ON p.idProducto = i.idProducto WHERE d.idPersona = 315 AND i.tipoimagen = 0 ORDER BY idProductoD ASC; 
       
        resultados = (
            db.session.query(ProductoDeseado, Producto, Imagen)
            .join(Producto, ProductoDeseado.idProducto == Producto.idProducto)
            .join(Imagen, Producto.idProducto == Imagen.idProducto)
            .filter(ProductoDeseado.idPersona == current_user.idPersona, Imagen.tipoImagen == 0)
            .order_by(ProductoDeseado.idProductoDeseado.asc())
            .all()
        )
      
        return render_template('/agregados/favoritos.html' , productos=resultados)
    return render_template('/agregados/favoritos.html' )    

@bp.route('/productos_deseados/acciones',  methods=['POST','GET'])
def acciones():
    
    
    if current_user.is_authenticated and  request.method == 'POST': 
        
        idProductoDeseado = request.form['fIdProductoDeseado']
        accion = request.form['fAccion']
    
        if accion == "Ingresar":       
            return insertar()
        
        elif accion == "EliminarTodo":
           eliminarTodo()  
            
        return redirect(url_for('bp_favoritos.index'))
    return redirect(url_for('bp_inicio.index'))


def insertar():
    
    return "funcion insertar"


def eliminarTodo():
    
    db.session.query(ProductoDeseado).delete()
    db.session.commit()
    
    
    

