from flask import Blueprint
bp = Blueprint('main', __name__)
from app.routes import index_routes
from app.routes import autenticacion_crear_routes

