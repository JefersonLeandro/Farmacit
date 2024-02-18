from flask import Blueprint, render_template , request , url_for , redirect, jsonify , flash , session
from flask_login import current_user
from app.routes.agregados_routes.carrito_routes import retornarResultados , calcularTotales
from app.models.Factura import Factura
from app.models.DetalleFactura import DetalleFactura 
from app import db
from datetime import date

bp = Blueprint('bp_factura', __name__)

@bp.route('/carrito_compras/factura' ,  methods=['GET'])
def index():
    if current_user.is_authenticated :
        #** modularizar codigo donde primero halla una funcion para verificar datos y si sale bien llamar la que procesa la factura 
        #** hacer ajax puede que funcione 
        #* actulizar las cantiades de los otros usuarios 
        
        resultados = retornarResultados()
        idPersona  = current_user.idPersona
   
        if resultados: 
            
            productosAgotados = []
            stockSuperado = False 
          
           
            for carrito , producto , Imagen  in resultados :
                
                idProducto = producto.idProducto
                stockProducto = producto.stockProducto
                cantidad = carrito.cantidadCarrito
               
                if stockProducto > 0 and stockProducto < cantidad: 
               
                    stockSuperado = True
                    carrito.cantidadCarrito = stockProducto
                    
                elif stockProducto == 0: 
                   
                    productosAgotados.append(producto.nombreProducto)
                    db.session.delete(carrito)
                
            if not(stockSuperado) and not(productosAgotados):
                
                # * actualiczar las cantidades de cada usuario para los productos comprados
                
                diccionario = calcularTotales()  
                
                nuevaFactura = Factura(idFactura = None, idPersona=idPersona, totalCompra = diccionario["total"], fechaCompra = date.today())
                db.session.add(nuevaFactura)
                db.session.commit()
               
                idFactura = nuevaFactura.idFactura
                
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
                    
                db.session.commit()
                    
                flash("Gracias por elegirnos , compra realizada correctamente  ","compraExito") 

               
            else:
               
                db.session.commit()
                # Filtrar productos agotados de los resultados, solo dejar producto disponibles 
                resultados = [res for res in resultados if res[1].stockProducto > 0]
                              
                
                if  not productosAgotados : 
                    productosAgotados = "noHayAgotados"
                
                if productosAgotados : 
                   
                    flash("Lo sentimos, algun producto se agoto, revisa y vuelve a procesar el pago   ","sinStock") 
                    
                if stockSuperado: 
                    flash("Lo sentimos, algun producto supero el stock, revisa y vuelve a procesar el pago ","stockSuperado") 
                    
                diccionario = calcularTotales()  
                
                return render_template('agregados/carrito.html',diccionario=diccionario , productos=resultados, productosAgotados = productosAgotados)
    return render_template('/agregados/carrito.html')                   
    
    
    
