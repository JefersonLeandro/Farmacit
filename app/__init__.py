from .models.Persona import Persona
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask import Flask
from .extensiones import db
import os 
from app.routes import index_routes
from app.routes.autenticacion_routes import crear_cuenta_routes, login_routes
from app.routes.area_Administracion_routes import index_routes as administracion_index_routes , farmacias_routes , personas_routes , roles_routes , productos_routes , marcas_productos_routes , imagenes_routes , facturas_routes , detalles_facturas_routes
from app.routes.agregados_routes import favoritos_routes , carrito_routes , factura_routes, producto_routes

login_manager = LoginManager()


migrate = Migrate()

def create_app():

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object('config.Config')
    bcrypt = Bcrypt(app)
    
    #Configurar la URI de la base de datos para usar SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/DbFarmacit'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Instancias de SQLAlchemy y Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'bp_inicio.index'
    
    
    @login_manager.user_loader
    def load_user(idPersona): # Flask-Login intentará cargar al usuario actual basándose en su identificador.
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Persona.query.get(int(idPersona))
    
    # se registran los blueprint de las rutas 
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(login_routes.bp)
    app.register_blueprint(crear_cuenta_routes.bp)
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