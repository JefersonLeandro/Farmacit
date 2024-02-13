from flask import Blueprint, render_template , request , url_for , redirect, jsonify
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
      
        resultados = (
            db.session.query(CarritoCompra, Producto, Imagen)
            .join(Producto, CarritoCompra.idProducto == Producto.idProducto)
            .join(Imagen, Producto.idProducto == Imagen.idProducto)
            .filter(CarritoCompra.idPersona == current_user.idPersona, Imagen.tipoImagen == 0)
            .order_by(CarritoCompra.idCarrito.asc())
            .all()
        )
        
        #me devuelve un diccionario 
        diccionario  = calcularTotales(resultados)
        
        return render_template('/agregados/carrito.html' , diccionario=diccionario , productos=resultados)    
    return render_template('/agregados/carrito.html')

@bp.route('/carrito_compras/insertar', methods=['POST','GET'])
def insertar():
    # *no dejar insertar productos que vayan a superar el stock de l producto
    if current_user.is_authenticated and  request.method == 'POST': 
    
        idProducto = request.form.get('fIdProducto', 0)
        consulta  = CarritoCompra.query.filter_by(idProducto=idProducto, idPersona=current_user.idPersona).first()
        
        
        if not consulta : 
            # inserta
            verificacion = Producto.query.filter_by(idProducto=idProducto).first()
             
            if verificacion : 
                
                nuevoCarrito = CarritoCompra(idCarrito = None, idPersona = current_user.idPersona , idProducto = idProducto , cantidadCarrito=1  )
                db.session.add(nuevoCarrito)
            
        else:
            #actualiza la cantidad del carrito encontrado 
            
            cantidad = consulta.cantidadCarrito + 1  
            consulta.cantidadCarrito = cantidad
            
        try:
            db.session.commit()
        except IntegrityError:
            # Se producirá una excepción si hay una violación de restricción única
            db.session.rollback() 
    
    return redirect(url_for('bp_inicio.index'))

def calcularTotales(resultados):
        
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
      
    cantidad = data['cantidad'].strip()
    idCarrito = data['idCarrito'].strip()
    
    
    
    if cantidad and idCarrito and (not cantidad.isspace()) and (not idCarrito.isspace()):
        # Hacer algo con los datos
            respuesta = {'mensaje': f'¡Datos recibidossss {data} correctamente cantidad {cantidad} idCarrito : {idCarrito}  !'}
            return jsonify(respuesta)

    else:
        respuesta = {'mensaje': '######DATOS-VACIOS#########' }
        return jsonify(respuesta)
    
    
    
    
    
    
    

    # respuesta = {'mensaje': f'¡Datos recibidos {data} correctamente cantidad {cantidad} idCarrito : {idCarrito}  !'}
    # return jsonify(respuesta)
  

    # Si 'dato' no está presente en los datos recibidos, devolver un error
        # return jsonify({'error': 'Campo "dato" no encontrado en los datos recibidos'}), 400

    #   if (not cantidad.isspace()) and (not idCarrito.isspace()):
    #     # Hacer algo con los datos
       
    #     if isinstance(cantidad (int)) and isinstance(idCarrito (int)):
    #         # La variable cantidad es un número (entero)
    #         respuesta = {'mensaje': f'¡Datos recibidos {data} correctamente ENTEROS cantidad {cantidad} idCarrito : {idCarrito}  !'}
    #         return jsonify(respuesta)
    #     else: 
    #         respuesta = {'mensaje' : 'NO SON ENTEROS '}
    #         return jsonify(respuesta)
            
    
    # else:
    #     respuesta = {'mensaje': '######DATOS-VACIOS#########' }
   
    #     return jsonify(respuesta)
    
    



