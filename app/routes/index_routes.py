from flask import Blueprint, render_template
from app.models.Producto import Producto
from app.models.MarcaProducto import MarcaProducto
from app import db

bp = Blueprint('bp_inicio', __name__)

@bp.route('/')
def index():
    
    productos = Producto.query.all()
    marcasProductos = MarcaProducto.query.all()
    
    return render_template('index.html', productos = productos, marcasProductos = marcasProductos )    




