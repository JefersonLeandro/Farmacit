from flask import Blueprint, render_template, request ,flash ,  redirect, url_for
from app.models import Imagen , Producto
from sqlalchemy import or_
from app import db
import os 


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
    
    imagen = request.files["fArchivoImagen"]
    nombreImagen =  imagen.filename 
    tipoImagen = request.form['fTipoImagen']
    
    idProducto = request.form['fIdProducto']
    consulta   = Producto.query.filter_by(idProducto=idProducto).first()
    
    guardarImagen(imagen , nombreImagen)
    
    if consulta is not None :
        
        nuevaImagen = Imagen(idImagen= None, nombreImagen = nombreImagen , tipoImagen = tipoImagen, idProducto = idProducto)
        db.session.add(nuevaImagen)
        db.session.commit()
        
    else : 
        flash('Imagen no insertada, idProducto no encontrado', 'idNoEncontrado')
    
def modificar(idImagen):
    
    imagen = Imagen.query.get_or_404(idImagen)
    
    imagen.nombreImagen = request.form['fArchivoImagen']
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