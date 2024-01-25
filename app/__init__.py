from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    # se registran los blueprint de las rutas 
    from app.routes import index_routes
    app.register_blueprint(index_routes.bp)
   
    return app