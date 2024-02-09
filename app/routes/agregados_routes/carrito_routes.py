from flask import Blueprint, render_template
from app import db

bp = Blueprint('bp_carrito', __name__)

@bp.route('/carrito_compras')
def index():

    return render_template('/agregados/carrito.html')    




