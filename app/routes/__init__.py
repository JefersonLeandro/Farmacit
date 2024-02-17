from flask import Blueprint
bp = Blueprint('main', __name__)

from app.routes import index_routes
from app.routes.autenticacion_routes import crear_cuenta_routes , login_routes
from app.routes.area_Administracion_routes import index_routes as administracion_index_routes , farmacias_routes , personas_routes , roles_routes , productos_routes , marcas_productos_routes , imagenes_routes
from app.routes.agregados_routes import favoritos_routes , carrito_routes , factura_routes
 
