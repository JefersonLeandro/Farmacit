from flask import Blueprint, render_template , redirect , url_for , request , flash
from flask_login import current_user , login_required
from sqlalchemy.orm import aliased
from app.models.Imagen import Imagen 
from app.models.Producto import Producto 
from app.models.ProductoDeseado import ProductoDeseado
from app.models.CarritoCompra import CarritoCompra
from app import db
from sqlalchemy.exc import IntegrityError



bp = Blueprint('bp_favoritos', __name__)

@bp.route('/productos_deseados')
def index():
    
    if current_user.is_authenticated:
       
        resultados = (
            db.session.query(ProductoDeseado, Producto, Imagen)
            .join(Producto, ProductoDeseado.idProducto == Producto.idProducto)
            .join(Imagen, Producto.idProducto == Imagen.idProducto)
            .filter(ProductoDeseado.idPersona == current_user.idPersona, Imagen.tipoImagen == 0)
            .order_by(ProductoDeseado.idProductoDeseado.asc())
            .all()
        )
      
        return render_template('/agregados/favoritos.html' , productos=resultados)
    return render_template('/agregados/favoritos.html' )    

@bp.route('/productos_deseados/acciones',  methods=['POST','GET'])
@login_required
def acciones():
    
    
    if current_user.is_authenticated and  request.method == 'POST': 
        
        idProductoDeseado = request.form.get('fIdProductoDeseado', 0)
        accion = request.form['fAccion']
    
        if accion == "Ingresar":       
            return insertar()
        
        elif accion == "transferirFavorito": 
            
            return tranferirFavorito()
        
        elif accion == "Eliminar":
            eliminar(idProductoDeseado)    

        elif accion == "EliminarTodo":
           eliminarTodo()  
            
        return redirect(url_for('bp_favoritos.index'))
    return redirect(url_for('bp_inicio.index'))


def insertar():
    
    
    idProducto = request.form["fIdProducto"]
    productoDeseado = ProductoDeseado.query.filter_by(idProducto=idProducto, idPersona=current_user.idPersona).first()
    
    paginaAnterior=request.referrer

    if not productoDeseado:
        # si no exite lo inserta 
        nuevoProductoDeseado = ProductoDeseado(idProductoDeseado=None, idPersona=current_user.idPersona, idProducto=idProducto)
        db.session.add(nuevoProductoDeseado)
       
        try:
            db.session.commit()
        except IntegrityError:
            # Se producirá una excepción si hay una violación de restricción única
            db.session.rollback()  
        
    if paginaAnterior:
        return redirect(paginaAnterior)
                  
    return redirect(url_for('bp_inicio.index'))


def tranferirFavorito():
    
    idProducto = request.form['fIdProducto']
    idProductoDeseado = request.form['fIdProductoDeseado']
    
    consulta  = CarritoCompra.query.filter_by(idProducto=idProducto, idPersona=current_user.idPersona).first()
    verificacion = Producto.query.filter_by(idProducto=idProducto).first()
    
    stockDisponible = verificacion.stockProducto if verificacion else 0
    cantidad = consulta.cantidadCarrito if consulta else 1
    
    
    if not consulta : 
        # inserta     
        if verificacion :  
            
            if stockDisponible >= cantidad :      

                nuevoCarrito = CarritoCompra(idCarrito = None, idPersona = current_user.idPersona , idProducto = idProducto , cantidadCarrito=1  )
                db.session.add(nuevoCarrito)
                eliminar(idProductoDeseado)
                flash( " Producto agregado al carrito correctamente." , "agregado")
                
            else:
                    
                flash( "Producto no agregado, stock superado." , "stockSuperado")
                
    else:
        #actualiza la cantidad del carrito encontrado 
        if stockDisponible > cantidad :  
    
            cantidad = consulta.cantidadCarrito + 1  
            consulta.cantidadCarrito = cantidad
            eliminar(idProductoDeseado)
            flash( " Producto agregado al carrito correctamente. " , "agregado")
            
        else: 

            flash("Producto no agregado, stock superado.", "stockSuperado")

    try:
        db.session.commit()
    
    except IntegrityError:
        db.session.rollback() 
    
    return redirect(url_for('bp_favoritos.index'))



def eliminarTodo():
    
    id_persona = current_user.idPersona 
    db.session.query(ProductoDeseado).filter_by(idPersona=id_persona).delete()
    db.session.commit()
    
def eliminar(idProductoDeseado):
    
    productoDeseado = ProductoDeseado.query.get_or_404(idProductoDeseado)
    db.session.delete(productoDeseado)
    db.session.commit()
     
    
