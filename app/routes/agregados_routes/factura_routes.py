from flask import Blueprint, render_template , request , url_for , redirect, jsonify , flash
from flask_login import current_user
from app.routes.agregados_routes.carrito_routes import retornarResultados , calcularTotales
from app import db

bp = Blueprint('bp_factura', __name__)


@bp.route('/carrito_compras/factura' ,  methods=['POST','GET'])
def index():
    if current_user.is_authenticated:
        
        resultados = retornarResultados()
        idPersona  = current_user.idPersona
        if resultados : 
            
            productosAgotados = {}
            stockSuperado = False
           
            for carrito , producto , Imagen  in resultados :
                
                idProducto = producto.idProducto
                stockProducto = producto.stockProducto
                cantidad = carrito.cantidadCarrito
                  
                if stockProducto > 0 and stockProducto < cantidad: 
                  
                    stockSuperado = True
                    carrito.cantidadCarrito = stockProducto
                    db.session.commit()
                    
                elif stockProducto == 0: 
                    
                    
                    print("El stock")
                    productosAgotados["producto"] = producto
                    #* mandar un mensaje con el producto agotados o agostados
            
            
            if not(stockSuperado) and not(productosAgotados):
                #procesar la factura
                return "todo salio bien , listo para procesar la factura"
            
            
            elif stockSuperado or productosAgotados:

                if  not productosAgotados : 
                    productosAgotados = "noHayAgotados"
                    
                if stockSuperado: 
                    flash("Lo sentimos, algun producto supero el stock, revisa y vuelve a procesar el pago ","stockSuperado") 
                    
                diccionario = calcularTotales()  
                return render_template('agregados/carrito.html',diccionario=diccionario , productos=resultados, productosAgotados=productosAgotados)
                
            

          
                
                
                
                      
            return "termino"
             
            print("nombre : ", producto.nombreProducto)
        
        return "llegueeeeeeeeeeeeeeeeeeeeee "
            
    return render_template('/agregados/carrito.html')
