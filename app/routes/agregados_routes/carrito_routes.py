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
        
        #me devuelve un diccionario 
        diccionario  = calcularTotales()
        
        #me devuelve los valores de bd 
        resultados = retornarResultados()
        
        return render_template('/agregados/carrito.html' , diccionario=diccionario , productos=resultados)    
    return render_template('/agregados/carrito.html')

@bp.route('/carrito_compras/insertar', methods=['POST','GET'])
def insertar():
    # *no dejar insertar productos que vayan a superar el stock de l producto
    if current_user.is_authenticated and  request.method == 'POST': 
    
        idProducto = request.form.get('fIdProducto', 0)
        consulta  = CarritoCompra.query.filter_by(idProducto=idProducto, idPersona=current_user.idPersona).first()
        verificacion = Producto.query.filter_by(idProducto=idProducto).first()
        
        
        if not consulta : 
            # inserta     
            if verificacion :         
                nuevoCarrito = CarritoCompra(idCarrito = None, idPersona = current_user.idPersona , idProducto = idProducto , cantidadCarrito=1  )
                db.session.add(nuevoCarrito)
            
        else:
            #actualiza la cantidad del carrito encontrado 
            stockDisponible = verificacion.stockProducto
            cantidad = consulta.cantidadCarrito
            
            if stockDisponible > cantidad :  
        
                cantidad = consulta.cantidadCarrito + 1  
                consulta.cantidadCarrito = cantidad
            else: 

                flash("Producto no agregado, stock superado")

        try:
            db.session.commit()
        except IntegrityError:
            # Se producirá una excepción si hay una violación de restricción única
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
            
            
            # respuesta = {'exito': f'----exito-- cantidad : {cantidad} y  idCarrito : {idCarrito}' }
            # carrito
            carritoEncontrado = CarritoCompra.query.filter_by(idCarrito=idCarrito , idPersona=current_user.idPersona).first()
            idProducto = carritoEncontrado.idProducto
            
            if carritoEncontrado:
                  
                # producto
                productoEncontrado = Producto.query.filter_by(idProducto = idProducto).first()
                stockProducto = productoEncontrado.stockProducto
                
                if stockProducto >= cantidad:    
                    
                    #update de cantidad carrito 
                                       
                    carritoEncontrado.cantidadCarrito = cantidad
                    db.session.commit()
                    
                    resultados = calcularTotales()
                    
                    respuesta = {f'resultados': resultados , 'stockProducto':stockProducto }
                    return jsonify(respuesta)
                    # actualizar la cantidad solo y si la cantidad es menor a que el stock de ese producto 
                    respuesta = {'mensaje': f'¡Datos recibidossss {data} correctamente cantidad {cantidad} idCarrito : {idCarrito}  !'}
                    return jsonify(respuesta)
                else: 
                   respuesta = {'stockSuperado': stockProducto}
                   return jsonify(respuesta)
                    
    
                 
    respuesta = {'fallo': 404 }
    return jsonify(respuesta)
    
    
    

        
 
    
        
              
            
        
       
     



