from app.extensiones import db
from sqlalchemy import UniqueConstraint

class ProductoDeseado (db.Model):
    __tablename__ = "ProductosDeseados" 
    idProductoDeseado=db.Column(db.Integer, primary_key=True)
    idPersona =db.Column(db.Integer, db.ForeignKey('Personas.idPersona'), nullable=False )
    idProducto =db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    __table_args__ = (UniqueConstraint('idProducto', 'idPersona'), )#datos unicos no se pueden repetir 