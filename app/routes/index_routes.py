from flask import Blueprint, render_template
from app.models import Producto , Imagen
from app.models.MarcaProducto import MarcaProducto
from sqlalchemy.orm import aliased
from app import db

bp = Blueprint('bp_inicio', __name__)

@bp.route('/')
def index():
    

    aliasImagen = aliased(Imagen)

    productosImagenPrimaria = (
        db.session.query(Producto)
        .join(aliasImagen, Producto.imagenes)
        .filter(aliasImagen.tipoImagen == 0)
        .distinct()
        .all()
    )
    marcasProductos = MarcaProducto.query.all()
    
    
    # for p in productosImagenPrimaria:
    #     for imagen in p.imagenes:
    #         print(f"++++++++ nombre: {p.nombreProducto} Imagen: {imagen.nombreImagen}")

        
    return render_template('index.html', productos = productosImagenPrimaria, marcasProductos = marcasProductos )    




