from app.extensiones import db

class Farmacia (db.Model):
    __tablename__ = "Farmacias"
    idFarmacia =  db.Column(db.Integer, primary_key=True) 
    nitFarmacia =  db.Column(db.String(45), nullable=False)
    nombreFarmacia = db.Column(db.String(45), nullable=False)
    telefonoFarmacia = db.Column(db.String(45), nullable=False)
    correoFarmacia =  db.Column(db.String(255), nullable=False)
    ubicacionFarmacia =  db.Column(db.String(255), nullable=False)