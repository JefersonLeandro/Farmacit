from app import db
from sqlalchemy.orm import relationship

class Producto (db.Model):
    
    idProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String(45), nullable=False)
    descripcionUnidad = db.Column(db.String(45), nullable=False)
    descripcionGeneral = db.Column(db.Text, nullable=False)
    stockProducto = db.Column(db.Integer, nullable=False)
    precioProducto = db.Column(db.Integer, nullable=False)
    idMarcaProducto = db.Column(db.Integer, db.ForeignKey('MarcaProducto.id'))

    