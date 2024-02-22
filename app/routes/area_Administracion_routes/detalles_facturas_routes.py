from flask import Blueprint, render_template , url_for , redirect
from flask_login import current_user , login_required
from app.models.DetalleFactura import DetalleFactura

bp = Blueprint('bp_detallesFacturas', __name__)

@bp.route('/area_administracion/facturas/detalles_facturas' , methods=['POST', 'GET'])
@login_required
def index():
    
    # listar detalles facturas
    if current_user.is_authenticated and current_user.idRol == 3: 
        detallesFacturas = DetalleFactura.query.all()
        return render_template('/areaAdministracion/detalles_facturas.html' , detallesFacturas= detallesFacturas)
    return redirect(url_for('bp_inicio.index'))
    