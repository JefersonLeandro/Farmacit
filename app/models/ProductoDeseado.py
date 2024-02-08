from app.extensiones import db

class ProductoDeseado (db.Model):
    __tablename__ = "ProductosDeseados" 
    idProductoDeseado=db.Column(db.Integer, primary_key=True)
    idPersona =db.Column(db.Integer, db.ForeignKey('Personas.idPersona'), nullable=False)
    idProducto =db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    