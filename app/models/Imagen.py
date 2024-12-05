from app.extensiones import db
from sqlalchemy.orm import relationship

class Imagen (db.Model):
    
    __tablename__ = "Imagenes"
    idImagen = db.Column(db.Integer, primary_key=True)
    nombreImagen = db.Column(db.String(255), nullable=False)
    tipoImagen = db.Column(db.SmallInteger, nullable=False)
    idProducto = db.Column(db.Integer,  db.ForeignKey('Productos.idProducto'),  nullable=False)
 

    