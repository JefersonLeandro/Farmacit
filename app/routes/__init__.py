from flask import Blueprint
bp = Blueprint('main', __name__)

from app.routes import index_routes
from app.routes import crear_cuenta_routes
from app.routes import login_routes

