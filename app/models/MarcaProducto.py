from app.extensiones import db


class MarcaProducto (db.Model):
    __tablename__ = "MarcasProductos" 
    idMarcaProducto = db.Column(db.Integer, primary_key=True)
    nombreMarca = db.Column(db.String(45), nullable=False)
    rs_producto = db.relationship('Producto', backref='marca', lazy=True)