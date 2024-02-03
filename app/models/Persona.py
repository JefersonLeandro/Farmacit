from flask_login import UserMixin
from app.extensiones import db

class Persona (db.Model, UserMixin):
    
    __tablename__ = "Personas"
    idPersona = db.Column(db.Integer, primary_key=True)
    nombrePersona = db.Column(db.String(45), nullable=False)
    apellidoPersona = db.Column(db.String(45), nullable=False)
    identificacionPersona = db.Column(db.String(15), nullable=False)
    correoPersona = db.Column(db.String(255), nullable=False)
    telefonoPersona = db.Column(db.String(15), nullable=False)
    contrasenaPersona = db.Column(db.String, nullable=False)
    idRol =db.Column(db.Integer, db.ForeignKey('Roles.idRol'))
    
    def get_id(self):
        return str(self.idPersona)
    
    # is_authenticated: 
    #     Devuelve True si el usuario está autenticado, es decir, si ha proporcionado credenciales válidas.

    # is_active: 
        # Devuelve True si el usuario está activo, generalmente se utiliza para realizar comprobaciones adicionales
        # sobre el estado del usuario.

    # is_anonymous:
    #     Devuelve False para usuarios autenticados, ya que no son anónimos.

    # get_id: 
        # Debe devolver un identificador único del usuario. Flask-Login utiliza este método para obtener 
        # el identificador del usuario actual.

    