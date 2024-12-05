from flask import Blueprint, render_template , redirect , url_for , request , flash
from flask_login import current_user , login_required
from sqlalchemy.orm import aliased
from app.models.Imagen import Imagen 
from app.models.Producto import Producto 
from app.routes.index_routes import tamanoCarrito 
from app import db


bp = Blueprint('bp_producto', __name__)

@bp.route('/producto/<int:idProducto>', methods=['GET'])
def index(idProducto):

    producto = Producto.query.get_or_404(idProducto)
    
    if current_user.is_authenticated:
        
        cantidadTotal = tamanoCarrito()
        return render_template('agregados/producto.html',producto=producto, cantidadTotal=cantidadTotal)
    
    return render_template('agregados/producto.html',producto=producto)
