from flask import Blueprint, render_template
from app.models.Producto import Producto 
from app.models.Imagen import  Imagen
from app.models.MarcaProducto import MarcaProducto
from sqlalchemy.orm import aliased
from app import db

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
  
    return render_template('index.html', productos= productosImagenPrimaria, marcasProductos = marcasProductos )    




