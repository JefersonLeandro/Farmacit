from flask import Blueprint, render_template  , url_for , redirect
from flask_login import current_user
from app.models.Factura import Factura

bp = Blueprint('bp_administracion_facturas', __name__)

@bp.route('/area_administracion/facturas' , methods=['POST', 'GET'])
def index():
    
    # listar facutuas
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        facturas = Factura.query.all()
        return render_template('/areaAdministracion/Facturas.html' , facturas = facturas)
    return redirect(url_for('bp_inicio.index'))
    