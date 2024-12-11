from flask import Blueprint, render_template , request , url_for , redirect, jsonify , flash , session , make_response
from flask_login import current_user , login_required
from app.routes.agregados_routes.carrito_routes import retornarResultados , calcularTotales
from app.models.Factura import Factura
from app.models.DetalleFactura import DetalleFactura 
from app.models.CarritoCompra import CarritoCompra 
from app import db
from datetime import date

bp = Blueprint('bp_factura', __name__)

@bp.route('/carrito_compras/factura' ,  methods=['GET'])
@login_required
def index():
    if current_user.is_authenticated :
        
        resultados = retornarResultados()
        idPersona  = current_user.idPersona
    
        if resultados: 
            
            global productosAgotados
            productosAgotados = [] # limpiarlos para la siguiente recarga   
                  
            verificar = verificarFactura(resultados)
           
            if not (verificar):
                #exito
                
                diccionario = calcularTotales()  
                
                nuevaFactura = Factura(idFactura = None, idPersona=idPersona, totalCompra = diccionario["total"], fechaCompra = date.today())
                db.session.add(nuevaFactura)
                db.session.commit()
               
                idFactura = nuevaFactura.idFactura
                
                informacionCompra = {}
                
                for carrito , producto , Imagen  in resultados :
                    
                    idProducto = producto.idProducto
                    precio = producto.precioProducto
                    cantidad = carrito.cantidadCarrito 
                    
                    producto.stockProducto -= carrito.cantidadCarrito
                    
                    subtotal = (precio * cantidad)
                    iva = subtotal * 0.19
                    subtotal+=iva
                    
                    nuevoDetalle = DetalleFactura(idDetalleFactura = None, cantidadDetalleF=cantidad, subtotalDetalleF = subtotal, idProducto = idProducto, idFactura = idFactura)
                    db.session.add(nuevoDetalle)    
                    db.session.delete(carrito)
                    
                    informacionCompra[f"{idProducto}"] = producto.stockProducto
                    
                db.session.commit()
                print(informacionCompra)
                
                productosAgotados = [] #vacia los productos agotados
                actualizarCantidades(informacionCompra)
         
                flash("Gracias por elegirnos, compra realizada correctamente. ","compraExito") 

            else:
                db.session.commit() #confirmar cambios de verificar Factura

                # Filtrar productos agotados de los resultados, solo dejar producto disponibles 
                resultados = [res for res in resultados if res[1].stockProducto > 0] 
            
                diccionario = calcularTotales()  
                return redirect(url_for('bp_carrito.index'))
        
    return render_template('/agregados/carrito.html')                   
    

def verificarFactura(resultados):
    
    verificar = False  
    stockSuperado = False 

    
    for carrito , producto , Imagen  in resultados :
        
        idProducto = producto.idProducto
        stockProducto = producto.stockProducto
        cantidad = carrito.cantidadCarrito
        
        if stockProducto > 0 and stockProducto < cantidad: 
        
            stockSuperado = True
            carrito.cantidadCarrito = stockProducto
            verificar = True
            
        elif stockProducto == 0: 
            
            productosAgotados.append(producto.nombreProducto)
            db.session.delete(carrito)
            verificar = True
        
    
    if productosAgotados : 
        flash("Lo sentimos, algun producto se agoto, revisa y vuelve a procesar el pago   ","sinStock") 
     
    if stockSuperado: 
        flash("Lo sentimos, algun producto supero el stock, revisa y vuelve a procesar el pago ","stockSuperado") 
        
    return verificar        

def actualizarCantidades(informacionCompra): 
    #actulizar las cantidades de todos los usuarios relacionados a ese producto en el carrito
    for id , stockDisponible in informacionCompra.items():
        
        carritos = CarritoCompra.query.filter_by(idProducto=id).all()
        
        if carritos: 
            for carrito in carritos:
     
                cantidad = carrito.cantidadCarrito
                if stockDisponible < cantidad : 
                    carrito.cantidadCarrito = stockDisponible 
            db.session.commit()