from app.extensiones import db
from sqlalchemy import UniqueConstraint


class CarritoCompra (db.Model):
    __tablename__ = "CarritoCompras" 
    idCarrito=db.Column(db.Integer, primary_key=True)
    idPersona =db.Column(db.Integer, db.ForeignKey('Personas.idPersona'), nullable=False)   
    idProducto =db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)   
    cantidadCarrito = db.Column(db.Integer, nullable=False)
    __table_args__ = (UniqueConstraint('idProducto', 'idPersona'), )#datos unicos no se pueden repetir 
    