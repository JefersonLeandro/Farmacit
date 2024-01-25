from flask import Blueprint, render_template
from app.models.Producto import Producto
# from app import db

bp = Blueprint('inicio', __name__)

@bp.route('/')
def index():
    
    # productos = Producto.query.all()
    
    return render_template('index.html' )    




