from flask import Blueprint, render_template, request , redirect, url_for
from flask_login import  current_user
from app.models import Farmacia
from app import db

bp = Blueprint('bp_farmacias', __name__)

@bp.route('/area_administracion/farmacias' , methods=['POST', 'GET'])
def index():
    # listar
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        farmacias = Farmacia.query.all()
        return render_template('/areaAdministracion/farmacias.html' , farmacias = farmacias)
    return redirect(url_for('bp_inicio.index'))
    

@bp.route('/area_administracion/farmacias/acciones', methods=['POST'])
def acciones():
    
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        if request.method == 'POST':
            idFarmacia = request.form['fIdFarmacia']
            accion = request.form['fAccion']
        
            if accion == "Ingresar":       
                insertar()
        
            elif accion == "Modificar":
                modificar(idFarmacia)
        
            elif accion == "Eliminar":
                eliminar(idFarmacia)  
        return redirect(url_for('bp_farmacias.index'))
    return redirect(url_for('bp_inicio.index'))
    
    
 
def insertar():
    
    nitFarmacia = request.form['fNitFarmacia']
    nombreFarmacia = request.form['fNombreFarmacia']
    telefonoFarmacia = request.form['fTelefonoFarmacia']
    correoFarmacia = request.form['fCorreoFarmacia']
    ubicacionFarmacia = request.form['fUbicacionFarmacia']
   
    nuevaFarmacia = Farmacia(idFarmacia = None, nitFarmacia=nitFarmacia, nombreFarmacia = nombreFarmacia, telefonoFarmacia = telefonoFarmacia, correoFarmacia = correoFarmacia, ubicacionFarmacia = ubicacionFarmacia)
    db.session.add(nuevaFarmacia)
    db.session.commit()
 
    
    
def modificar(idFarmacia):
    
    farmacia = Farmacia.query.get_or_404(idFarmacia)
    farmacia.nitFarmacia = request.form['fNitFarmacia']
    farmacia.nombreFarmacia = request.form['fNombreFarmacia']
    farmacia.telefonoFarmacia = request.form['fTelefonoFarmacia']
    farmacia.correoFarmacia = request.form['fCorreoFarmacia']
    farmacia.ubicacionFarmacia = request.form['fUbicacionFarmacia']
    
    db.session.commit()
      

def eliminar(idFarmacia):
    
    farmacia = Farmacia.query.get_or_404(idFarmacia)
    db.session.delete(farmacia)
    db.session.commit()
    



