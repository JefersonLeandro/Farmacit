from flask import Blueprint, render_template, request ,flash ,  redirect, url_for
from app.models import Imagen , Producto
from sqlalchemy import or_
from app import db


bp = Blueprint('bp_imagenes', __name__)

@bp.route('/area_administracion/productos/imagenes' , methods=['POST', 'GET'])
def index():
    # listar
    imagenes = Imagen.query.all()
    return render_template('/areaAdministracion/imagenes.html' , imagenes =imagenes )


@bp.route('/area_administracion/productos/imagenes/buscar' , methods=['POST', 'GET'])
def buscar():
    
    cadena = request.form['fValorBusqueda']

    # Consulta con condiciones combinadas
    productosEncontrados = Producto.query.filter(
        or_(
            Producto.nombreProducto.contains(cadena),
            Producto.descripcionUnidad.contains(cadena),
            Producto.descripcionProductoGeneral.contains(cadena)
        )
    ).all()

    imagenes = Imagen.query.all()
    
    if productosEncontrados :  
        return render_template('/areaAdministracion/imagenes.html',imagenes=imagenes,  productosEncontrados = productosEncontrados, cadena = cadena)
    else:
        flash('No se encontraron coincidencias', 'busquedaVacia')
        return render_template('/areaAdministracion/imagenes.html' ,imagenes=imagenes , cadena = cadena )  

@bp.route('/area_administracion/productos/imagenes/acciones', methods=['POST'])
def acciones():
    
    if request.method == 'POST':
        
        idImagen = request.form['fIdImagen']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
           insertar()
          
        elif accion == "Modificar":
           modificar(idImagen)
     
        elif accion == "Eliminar":
          eliminar(idImagen)    
         
   
    return redirect(url_for('bp_imagenes.index'))

def insertar():
    
    nombreImagen = request.form['fNombreImagen']
    tipoImagen = request.form['fTipoImagen']
    
    idProducto = request.form['fIdProducto']
    consulta   = Producto.query.filter_by(idProducto=idProducto).first()
    
    if consulta is not None :
        
        nuevaImagen = Imagen(idImagen= None, nombreImagen = nombreImagen , tipoImagen = tipoImagen, idProducto = idProducto)
        db.session.add(nuevaImagen)
        db.session.commit()
        
    else : 
        flash('Imagen no insertada, idProducto no encontrado', 'idNoEncontrado')
    
def modificar(idImagen):
    
    imagen = Imagen.query.get_or_404(idImagen)
    
    imagen.nombreImagen = request.form['fNombreImagen']
    imagen.tipoImagen = request.form['fTipoImagen'] 
    db.session.commit()
   
   
def eliminar(idImagen):
    
    imagen = Imagen.query.get_or_404(idImagen)
    db.session.delete(imagen)
    db.session.commit()
    