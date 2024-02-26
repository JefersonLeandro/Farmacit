from flask import Blueprint, render_template  , url_for , redirect , request
from flask_login import current_user , login_required 
from app.models.Factura import Factura
from app.models.DetalleFactura import DetalleFactura
from app.models.Persona import Persona

bp = Blueprint('bp_administracion_facturas', __name__)

@bp.route('/area_administracion/facturas' , methods=['POST', 'GET'])
def index():
    
    # listar facutuas
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        facturas = Factura.query.all()
        return render_template('/areaAdministracion/facturas.html' , facturas = facturas)
    return redirect(url_for('bp_inicio.index'))



# button ver detalles y que lo lleve a los tabla de detalles pero solo con esos detalles de aqui mismo crear un funcion 
@bp.route('/area_administracion/facturas/<int:idFactura>', methods=['GET'])
@login_required
def detallesEspecificos(idFactura):
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        detallesFactura =  DetalleFactura.query.filter_by(idFactura=idFactura).all()
        return render_template('/areaAdministracion/detalles_facturas.html' , detallesFacturas= detallesFactura)
    return redirect(url_for('bp_inicio.index'))
    

# hacer un buscar por documento 
@bp.route('/area_administracion/facturas/busqueda', methods=['POST','GET'])
@login_required
def busqueda():
        
    if current_user.is_authenticated and current_user.idRol == 3: 
    
        cadena = request.form['fCadena']

        # Filtrar las facturas por documento o nombre de la persona asociada
        # resultados = Factura.query.filter(
        #     (Factura.rs_persona.identificacionPersona.like(f'%{cadena}%')) | # (pipe) para representar la operación OR
        #     (Factura.rs_persona.nombrePersona.like(f'%{cadena}%'))
        # ).all()
        
        resultados = Factura.query.with_entities(
            Factura.idFactura,
            Factura.idPersona,
            Factura.totalCompra,
            Factura.fechaCompra, 
            Persona.nombrePersona
        ).join(Persona).filter(
            (Persona.identificacionPersona.like(f'%{cadena}%')) | # (pipe) para representar la operación OR
            (Persona.nombrePersona.like(f'%{cadena}%'))
        ).all()
        
        return render_template('/areaAdministracion/facturas.html' , facturas = resultados)
    return redirect(url_for('bp_inicio.index'))   
    