from flask import Blueprint, render_template


bp = Blueprint('bp_administracion', __name__)

@bp.route('/area_administracion')
def index():
    
    return render_template('/areaAdministracion/index.html' )    




