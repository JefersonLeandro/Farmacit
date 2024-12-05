from flask import Blueprint, render_template, request ,flash ,  redirect, url_for
from app.models import Imagen , Producto
from flask_login import current_user , login_required
from sqlalchemy import or_
from app import db
import os 


bp = Blueprint('bp_imagenes', __name__)

@bp.route('/area_administracion/productos/imagenes' , methods=['POST', 'GET'])
@login_required
def index():
    # listar
    
    if current_user.is_authenticated and current_user.idRol == 3: 
        imagenes = Imagen.query.all()
        return render_template('/areaAdministracion/imagenes.html' , imagenes =imagenes )    
    return redirect(url_for('bp_inicio.index'))


@bp.route('/area_administracion/productos/imagenes/buscar' , methods=['POST', 'GET'])
@login_required
def buscar():
    
    
    if current_user.is_authenticated and current_user.idRol == 3 and  request.method == 'POST': 
       
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
        
        if productosEncontrados:  
            return render_template('/areaAdministracion/imagenes.html',imagenes=imagenes,  productosEncontrados = productosEncontrados, cadena = cadena)
        else:
            flash('No se encontraron coincidencias', 'busquedaVacia')
            return render_template('/areaAdministracion/imagenes.html' ,imagenes=imagenes , cadena = cadena )  
    return redirect(url_for('bp_inicio.index'))

@bp.route('/area_administracion/productos/imagenes/acciones', methods=['POST' , 'GET'])
@login_required
def acciones():
    
    if current_user.is_authenticated and current_user.idRol == 3 and request.method == 'POST' : 
        
        idImagen = request.form['fIdImagen']
        accion = request.form['fAccion']
        
        if accion == "Ingresar":       
            insertar()
        
        elif accion == "Modificar":
            modificar(idImagen)
    
        elif accion == "Eliminar":
            eliminar(idImagen)    

        
        return redirect(url_for('bp_imagenes.index'))
    return redirect(url_for('bp_inicio.index'))

def insertar():
    
    imagen = request.files["fArchivoImagen"]
    nombreImagen =  imagen.filename 
    tipoImagen = request.form['fTipoImagen']
    
    idProducto = request.form['fIdProducto']
    consulta   = Producto.query.filter_by(idProducto=idProducto).first()
    
    
    if consulta is not None :
        
        guardarImagen(imagen , nombreImagen)
        
        nuevaImagen = Imagen(idImagen= None, nombreImagen = nombreImagen , tipoImagen = tipoImagen, idProducto = idProducto)
        db.session.add(nuevaImagen)
        db.session.commit()
        
    else : 
        flash('Imagen no insertada, idProducto no encontrado', 'idNoEncontrado')
    
def modificar(idImagen):
    
    imagen = Imagen.query.get_or_404(idImagen)
    
    imagen.tipoImagen = request.form['fTipoImagen'] 
    db.session.commit()
   
   
def eliminar(idImagen):

    from run  import app 
    imagen = Imagen.query.get_or_404(idImagen)    
    ruta_imagen = os.path.join(app.root_path, "static", "imagenes", imagen.nombreImagen)

    # Elimina la imagen del sistema de archivos
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
    
    db.session.delete(imagen)
    db.session.commit()

def guardarImagen(imagen , nombreImagen):
    from run  import app 
    carpetaDestino = os.path.join(app.root_path, "static" , "imagenes")    
    imagen.save(os.path.join(carpetaDestino, nombreImagen))