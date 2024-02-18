from flask import Blueprint, render_template , request , url_for , redirect, jsonify , flash
from app.models.Producto import Producto 
from app.models.CarritoCompra import CarritoCompra 
from app.models.Imagen import Imagen
from sqlalchemy.exc import IntegrityError
from flask_login import current_user
from app import db

bp = Blueprint('bp_carrito', __name__)


@bp.route('/carrito_compras')
def index():
    if current_user.is_authenticated:
        #* eliminar los carritos donde su stock es igual a cero y mandarlos a un array con los productos agotados
        
        #me devuelve un diccionario 
        diccionario  = calcularTotales()
        
        #me devuelve los valores de bd 
        resultados = retornarResultados()
        
        return render_template('/agregados/carrito.html' , diccionario=diccionario , productos=resultados)    
    return render_template('/agregados/carrito.html')

@bp.route('/carrito_compras/insertar', methods=['POST','GET'])
def insertar():
  
    if current_user.is_authenticated and  request.method == 'POST': 
    
        idProducto = request.form.get('fIdProducto', 0)
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
                else:
                     
                    flash( "Producto no agregado, stock superado" , "stockSuperado")
                    
        else:
            #actualiza la cantidad del carrito encontrado 
            if stockDisponible > cantidad :  
        
                cantidad = consulta.cantidadCarrito + 1  
                consulta.cantidadCarrito = cantidad
                
            else: 

                flash("Producto no agregado, stock superado", "stockSuperado")

        try:
            db.session.commit()
        
        except IntegrityError:
            db.session.rollback() 
    
    return redirect(url_for('bp_inicio.index'))

def retornarResultados():
    resultados = (
        db.session.query(CarritoCompra, Producto, Imagen)
        .join(Producto, CarritoCompra.idProducto == Producto.idProducto)
        .join(Imagen, Producto.idProducto == Imagen.idProducto)
        .filter(CarritoCompra.idPersona == current_user.idPersona, Imagen.tipoImagen == 0)
        .order_by(CarritoCompra.idCarrito.asc())
        .all()
    )
    
    return resultados


def calcularTotales():
    
    resultados = retornarResultados()
            
    subtotal = 0
    cantidadFinal = 0  
    for carrito , producto , Imagen  in resultados : 
        
        precio = producto.precioProducto
        cantidadProducto = carrito.cantidadCarrito
        
        cantidadFinal += cantidadProducto
        subtotal+= precio * cantidadProducto
    
    iva = subtotal * 0.19 
    total = iva + subtotal
    
    diccionario = { "subtotal" : round(subtotal,2) , "cantidadFinal" : cantidadFinal , "iva" : round(iva,2) , "total" : round(total,2)} 
    return diccionario

@bp.route('/carrito_compras/eliminar', methods=['POST','GET'])
def eliminarCarrito():
    
    if current_user.is_authenticated  and request.method == 'POST': 
        
        idCarrito = request.form['fIdCarrito']
        carrito = CarritoCompra.query.get_or_404(idCarrito)
        db.session.delete(carrito)
        db.session.commit()

    return redirect(url_for('bp_carrito.index'))


@bp.route('/carrito_compras/actulizar', methods=['POST'])
def actualizarCantidad():
    
    
    data = request.get_json()
      
    cantidad = str(data['cantidad'])
    idCarrito = str(data['idCarrito'])
    
    if cantidad and idCarrito and (not cantidad.isspace()) and (not idCarrito.isspace()) and cantidad.isdigit() and idCarrito.isdigit():
        
        cantidad = int(cantidad)
        idCarrito = int(idCarrito)
        
        if cantidad > 0  and  idCarrito > 0 :
            
            #carrito
            carritoEncontrado = CarritoCompra.query.filter_by(idCarrito=idCarrito , idPersona=current_user.idPersona).first()
            
            if carritoEncontrado:
                
                idProducto = carritoEncontrado.idProducto
                  
                # producto
                productoEncontrado = Producto.query.filter_by(idProducto = idProducto).first()
                stockProducto = productoEncontrado.stockProducto
                
                if stockProducto >= cantidad:    
                                      
                    carritoEncontrado.cantidadCarrito = cantidad
                    db.session.commit()
                    
                    resultados = calcularTotales()
                    respuesta = {f'resultados': resultados , 'stockProducto':stockProducto }
                    
                    return jsonify(respuesta)
           
                else: 
                    
                   respuesta = {'stockSuperado': stockProducto}
                   return jsonify(respuesta)
                    
    
                 
    respuesta = {'fallo': 404 }
    return jsonify(respuesta)
    
    
    

        
 
    
        
              
            
        
       
     



