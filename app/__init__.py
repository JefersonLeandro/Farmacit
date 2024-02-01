from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Flask
from .models.Persona import Persona, db
import os 

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object('config.Config')
    bcrypt = Bcrypt(app)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'bp_login.login'
    
    @login_manager.user_loader
    def load_user(idPersona): # Flask-Login intentará cargar al usuario actual basándose en su identificador.
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Persona.query.get(int(idPersona))
    
    
    from app.routes import index_routes, login_routes, crear_cuenta_routes

    # se registran los blueprint de las rutas 
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(login_routes.bp)
    app.register_blueprint(crear_cuenta_routes.bp)
   
    return app