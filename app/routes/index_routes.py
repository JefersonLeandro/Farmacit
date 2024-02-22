from flask import Blueprint, render_template , request, flash
from app.models.Producto import Producto 
from app.models.Imagen import  Imagen
from app.models.MarcaProducto import MarcaProducto
from app.models.CarritoCompra import CarritoCompra
from sqlalchemy.orm import aliased
from app import db
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_login import current_user

bp = Blueprint('bp_inicio', __name__)

@bp.route('/')
def index():

    productos = productosGenerales()
      
    marcasProductos = MarcaProducto.query.all()
    
    if current_user.is_authenticated : 
        cantidadTotal = tamanoCarrito()
        
        return render_template('index.html', productos= productos, marcasProductos = marcasProductos , cantidadTotal = cantidadTotal ) 
    return render_template('index.html', productos= productos, marcasProductos = marcasProductos )    

def tamanoCarrito():
    
    cantidadTotal = (
        db.session.query(func.sum(CarritoCompra.cantidadCarrito).label('cantidadTotal'))
        .filter(CarritoCompra.idPersona == current_user.idPersona)
        .scalar()  # scalar() para obtener el valor directamente
    )
    
    return cantidadTotal
    

@bp.route('/buscar' , methods=['POST'])
def buscar():
        
    cadena = request.form['fCadena']
    
    aliasImagen = aliased(Imagen)
    
    productosFiltrados = (  
        db.session.query(Producto)
        .join(aliasImagen, Producto.rs_Imagenes)
        .filter(
            (Producto.nombreProducto.like(f'%{cadena}%')) | # (pipe) para representar la operación OR
            (Producto.descripcionProductoGeneral.like(f'%{cadena}%'))
        )
        .filter(aliasImagen.tipoImagen == 0)
        .distinct()
        .all()
    )
    
    marcasProductos = MarcaProducto.query.all()
    
    if productosFiltrados:
        if current_user.is_authenticated : 
        
            cantidadTotal = tamanoCarrito()
            return render_template('index.html', productos= productosFiltrados, marcasProductos = marcasProductos , cantidadTotal = cantidadTotal )
        return render_template('index.html', productos= productosFiltrados, marcasProductos = marcasProductos )    
      
    else:  
        
        flash('No se encontraron concidencias.', 'sinConcidencias')
        productos = productosGenerales()
        
        if current_user.is_authenticated: 
            cantidadTotal = tamanoCarrito()
            return render_template('index.html', productos=productos, marcasProductos = marcasProductos, cantidadTotal = cantidadTotal)
        
        else: 
            return render_template('index.html', productos=productos, marcasProductos = marcasProductos )
           

def productosGenerales(): 
    
    aliasImagen = aliased(Imagen)

    productosImagenPrimaria = (
        db.session.query(Producto)
        .join(aliasImagen, Producto.rs_Imagenes)
        .filter(aliasImagen.tipoImagen == 0)
        .distinct()
        .all()
    )
    
    return productosImagenPrimaria 
    
    

