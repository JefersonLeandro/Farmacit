from flask import Blueprint, render_template
from app.models.Producto import Producto 
from app.models.Imagen import  Imagen
from app.models.MarcaProducto import MarcaProducto
from app.models.CarritoCompra import CarritoCompra
from sqlalchemy.orm import aliased
from app import db
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_login import current_user

bp = Blueprint('bp_inicio', __name__)

@bp.route('/')
def index():

    aliasImagen = aliased(Imagen)

    productosImagenPrimaria = (
        db.session.query(Producto)
        .join(aliasImagen, Producto.rs_Imagenes)
        .filter(aliasImagen.tipoImagen == 0)
        .distinct()
        .all()
    )
    marcasProductos = MarcaProducto.query.all()
    
    if current_user.is_authenticated : 
        
        cantidadTotal = (
            db.session.query(func.sum(CarritoCompra.cantidadCarrito).label('cantidadTotal'))
            .filter(CarritoCompra.idPersona == current_user.idPersona)
            .scalar()  # scalar() para obtener el valor directamente
        )
        
        return render_template('index.html', productos= productosImagenPrimaria, marcasProductos = marcasProductos , cantidadTotal = cantidadTotal )    
        
        
    return render_template('index.html', productos= productosImagenPrimaria, marcasProductos = marcasProductos )    




