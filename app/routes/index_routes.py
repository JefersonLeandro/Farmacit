from flask import Blueprint, render_template
from app.models.Producto import Producto
from app.models.MarcaProducto import MarcaProducto
from app import db

bp = Blueprint('inicio', __name__)

@bp.route('/')
def index():
    
    productos = Producto.query.all()
    marcasProductos = MarcaProducto.query.all()
    print(productos, "--iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii--")
    
    return render_template('index.html', productos = productos, marcasProductos = marcasProductos )    




