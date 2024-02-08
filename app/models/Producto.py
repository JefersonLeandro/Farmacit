from sqlalchemy.orm import relationship
from app.extensiones import db

class Producto (db.Model):
    
    __tablename__ = "Productos"
    idProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String(45), nullable=False)
    descripcionUnidad = db.Column(db.String(45), nullable=False)
    descripcionProductoGeneral = db.Column(db.Text, nullable=False)
    stockProducto = db.Column(db.Integer, nullable=False)
    precioProducto = db.Column(db.Integer, nullable=False)
    idMarcaProducto = db.Column(db.Integer, db.ForeignKey('MarcasProductos.idMarcaProducto') , nullable=False)
    rs_Imagenes = db.relationship('Imagen', backref='bk_producto', lazy=True)
    