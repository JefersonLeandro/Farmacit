from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = "miLlaveSecreta"
    app.config.from_object('config.Config')
    bcrypt = Bcrypt(app)
    db.init_app(app)

    from app.routes import index_routes
    from app.routes import autenticacion_crear_routes

    
    # se registran los blueprint de las rutas 
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(autenticacion_crear_routes.bp)
    
   
    return app