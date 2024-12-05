from app.extensiones import db

class DetalleFactura (db.Model):
    __tablename__ = "DetallesFacturas"
    idDetalleFactura =  db.Column(db.Integer, primary_key=True) 
    cantidadDetalleF =  db.Column(db.Integer, nullable=False)
    subtotalDetalleF =  db.Column(db.Integer, nullable=False)
    idProducto =db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    idFactura =db.Column(db.Integer, db.ForeignKey('Facturas.idFactura'), nullable=False)
    rs_productos = db.relationship('Producto', lazy=True)
    
  