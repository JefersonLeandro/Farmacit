from flask import Blueprint, render_template , redirect , url_for
from flask_login import  current_user

bp = Blueprint('bp_administracion', __name__)

@bp.route('/area_administracion')
def index():
    
    if current_user.is_authenticated and current_user.idRol == 3 : 
       
        return render_template('/areaAdministracion/index.html' )    
  
    return redirect(url_for('bp_inicio.index'))




