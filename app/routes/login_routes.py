from flask import Blueprint, render_template
# from routes.autenticacion_crear_routes import bp_autenticacion_crear
# from app.routes.autenticacion_crear_routes import bp_autenticacion_crear as bp
from flask_bcrypt import Bcrypt
from app import db

# bp = bp_autenticacion_crear
bp = Blueprint('bp_login', __name__)

@bp.route('/login') 
def login():
    return render_template('login.html')

@bp.route('/login/autenticacion') 
def autenticacion():
    
    
    return "login en proceso para verificar"
