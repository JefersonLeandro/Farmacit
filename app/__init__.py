from flask_login import LoginManager
from flask import Flask
from .extensiones import db
import os 
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.login_view = 'bp_inicio.index'
    login_manager.init_app(app)

    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'Farmacit.envio.correos@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xfor bgnv fixj hvql'

    mail = Mail(app) 

    @login_manager.user_loader
    def load_user(idPersona): # Flask-Login intentará cargar al usuario actual basándose en su identificador.
        from .models.Persona import Persona
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Persona.query.get(int(idPersona))
    

    from app.routes import index_routes
    from app.routes.autenticacion_routes import crear_cuenta_routes, login_routes, validacion_correo_electronico
    from app.routes.area_Administracion_routes import index_routes as administracion_index_routes , farmacias_routes , personas_routes , roles_routes , productos_routes , marcas_productos_routes , imagenes_routes , facturas_routes , detalles_facturas_routes
    from app.routes.agregados_routes import favoritos_routes , carrito_routes , factura_routes, producto_routes

    # se registran los blueprint de las rutas 
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(login_routes.bp)
    app.register_blueprint(crear_cuenta_routes.bp)
    app.register_blueprint(validacion_correo_electronico.bp)
    app.register_blueprint(administracion_index_routes.bp)
    app.register_blueprint(farmacias_routes.bp)
    app.register_blueprint(personas_routes.bp)
    app.register_blueprint(roles_routes.bp)
    app.register_blueprint(productos_routes.bp)
    app.register_blueprint(marcas_productos_routes.bp)
    app.register_blueprint(imagenes_routes.bp)
    app.register_blueprint(favoritos_routes.bp)
    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(factura_routes.bp)
    app.register_blueprint(facturas_routes.bp)
    app.register_blueprint(detalles_facturas_routes.bp)
    
    app.register_blueprint(producto_routes.bp)
   
    return app