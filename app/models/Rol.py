from app.extensiones import db

class Rol (db.Model):
    __tablename__ = "Roles" 
    idRol=db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String(45), nullable=False)    