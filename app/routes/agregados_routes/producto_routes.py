from flask import Blueprint, render_template , redirect , url_for , request , flash
from flask_login import current_user , login_required
from sqlalchemy.orm import aliased
from app.models.Imagen import Imagen 
from app.models.Producto import Producto 
from app import db


bp = Blueprint('bp_producto', __name__)

@bp.route('/producto/<int:idProducto>', methods=['GET'])
def index(idProducto):
    #  resultados = (
    #     db.session.query(CarritoCompra, Producto, Imagen)
    #     .join(Producto, CarritoCompra.idProducto == Producto.idProducto)
    #     .join(Imagen, Producto.idProducto == Imagen.idProducto)
    #     .filter(CarritoCompra.idPersona == current_user.idPersona, Imagen.tipoImagen == 0)
    #     .order_by(CarritoCompra.idCarrito.asc())
    #     .all()
    # )
    
    producto = (
        db.session.query(Producto, Imagen)
        .join(Producto, Producto.idProducto==Imagen.idProducto)
        .where(Imagen.idProducto == idProducto)
        .order_by(Imagen.idImagen.desc())
        .all()
    )
    return render_template('agregados/producto.html',producto=producto)
