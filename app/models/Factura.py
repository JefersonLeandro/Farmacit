from app.extensiones import db

class Factura (db.Model):
    __tablename__ = "Facturas"
    idFactura =  db.Column(db.Integer, primary_key=True) 
    idPersona =db.Column(db.Integer, db.ForeignKey('Personas.idPersona'), nullable=False)
    totalCompra =  db.Column(db.Integer, nullable=False)
    fechaCompra =  db.Column(db.Date, nullable=False)
