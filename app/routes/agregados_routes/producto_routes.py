from flask import Blueprint, render_template , redirect , url_for , request , flash
from flask_login import current_user , login_required
from sqlalchemy.orm import aliased
from app.models.Imagen import Imagen 
from app.models.Producto import Producto 
from app import db


bp = Blueprint('bp_producto', __name__)

@bp.route('/producto/<int:idProducto>', methods=['GET'])
def index(idProducto):
    
    producto = (
        db.session.query(Producto, Imagen)
        .join(Producto, Producto.idProducto==Imagen.idProducto)
        .where(Imagen.idProducto == idProducto)
        .order_by(Imagen.idImagen.desc())
        .all()
    )
    return render_template('agregados/producto.html',producto=producto)
