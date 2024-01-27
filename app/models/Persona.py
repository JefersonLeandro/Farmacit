from app import db


class Persona (db.Model):
    
    __tablename__ = "Personas"
    idPersona = db.Column(db.Integer, primary_key=True)
    nombrePersona = db.Column(db.String(45), nullable=False)
    apellidoPersona = db.Column(db.String(45), nullable=False)
    identificacionPersona = db.Column(db.String(15), nullable=False)
    correoPersona = db.Column(db.String(120), nullable=False)
    telefonoPersona = db.Column(db.String(15), nullable=False)
    contrasenaPersona = db.Column(db.String, nullable=False)
    idRol = db.Column(db.Integer, db.ForeignKey('Roles.idRol'))

    