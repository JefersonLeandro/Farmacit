
    //eventos 

    const liFactura = document.querySelector(".carrito-li-factura"),
          seccionFactura = document.querySelector(".carrito-info"),
          svgCerrar = document.querySelector("#svgCerrar");
    
    //alerta
    liFactura.addEventListener('click', function () {
        seccionFactura.classList.add('active');
    });
    svgCerrar.addEventListener('click', function () {
        seccionFactura.classList.remove('active');
     
    });


    //inputs

    let inputs = document.querySelectorAll(".carrito-inputCantidad");
    inputs.forEach(function (input) {
        input.addEventListener("click", function (event) {
            event.preventDefault(); // Evitar el comportamiento predeterminado del evento
            //se seleciona dentro del contenedor el btn a actualizar 
            let botonActualizar = input.closest(".carrito-subCaja1-1").querySelector(".carrito-btnActualizar");
            // var botonActualizar = input.parentNode.querySelector(".carrito-btnActualizar");

            if (botonActualizar.style.display != "block") {
                botonActualizar.style.display = "block";
            }
            cantidad = input.value
            console.log("click input-cantidad : " + input.value);
        });
    });

    //botones
    const botones = document.querySelectorAll("button.carrito-btnActualizar");
    botones.forEach(function (boton) {
        boton.addEventListener("click", function (event) {
            event.preventDefault();  // Evitar el comportamiento predeterminado del evento
            console.log("click btn-actualizar ");

            const input = boton.closest(".carrito-subCaja1-1").querySelector(".carrito-inputCantidad");
            const stock_Producto = boton.closest(".carrito-subCaja1-1").querySelector(".carrito-inputStock");
            const id_Carrito = boton.closest(".carrito-subCaja1-1").querySelector(".carrito-inputIdCarrito");
            console.log(" idCarrito  : " + id_Carrito);

            let cantidad = input.value.trim();
            let stockProducto = stock_Producto.value.trim();
            let idCarrito = id_Carrito.value.trim();

            if ((cantidad !== null && cantidad.replace(/\s/g, '') !== "") && (stockProducto !== null && stockProducto.replace(/\s/g, '') !== "") && (idCarrito !== null && idCarrito.replace(/\s/g, '') !== "") ){

                comprobar = verificacion(cantidad, stockProducto , idCarrito); 
               
                if (comprobar) {

                    actualizarCantidadAjax(cantidad, idCarrito, input, boton)

                } else if (comprobar === false) {

                    input.value = 1;

                } else {

                    window.alert("stock disponible :  " + stockProducto)
                    input.value = stockProducto;
                }

            }else{
             input.value = 1;
            }
        });
    });



    function verificacion(cantidadAsociada, stock_Producto, id_Carrito) {


        // Expresión regular que coincide con cualquier cosa que no sea un número
        let expresionRegular = /[^0-9]/;

        // Verificar si la cadena contiene caracteres que no son números
        let test = expresionRegular.test(cantidadAsociada); // true a2b4ca, false 123123 

        let bandera = false;

        if (!(test)) {//false

            let cantidad = parseInt(cantidadAsociada, 10);
            let stockProducto = parseInt(stock_Producto, 10)
            let idCarrito = parseInt(id_Carrito, 10)

            console.log("stock PRODUCTO INT " + stockProducto)
            console.log("id Carrito  INT " + idCarrito)

            if (stockProducto > 0 && idCarrito > 0) {

                if (!isNaN(cantidad) && cantidad > 0) {

                    if (cantidad <= stockProducto) {

                        bandera = true;

                    } else {

                        bandera = null;
                    }
                }

            } else {
                window.location.reload();
            }
        }

        return bandera
    }


    function actualizarCantidadAjax(cantidadAsociada, id_Carrito, input, boton) {
        // Crear objeto XMLHttpRequest
        var xhr = new XMLHttpRequest();
        let cantidad = parseInt(cantidadAsociada, 10);

        let idCarrito = parseInt(id_Carrito, 10);

        // Configurar la solicitud
        xhr.open('POST', '/carrito_compras/actulizar', true);
        xhr.setRequestHeader('Content-Type', 'application/json');  // Cambiar el tipo de contenido a JSON
        // Configurar la función de devolución de llamada
        boton.disabled = true;
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    boton.disabled = false
                    boton.style.display = "none";

                    //seleccion 
                    const stock_Producto = boton.closest(".carrito-subCaja1-1").querySelector(".carrito-inputStock");
                    let small_stock = boton.closest(".carrito-cajaMediana").querySelector(".smallStock");
                    
                    stockActual = stock_Producto.value 

                    let respuesta = JSON.parse(xhr.responseText);
                    
                    //controlar la respuesta 
                    if (respuesta.hasOwnProperty("resultados") ){
                        //recibir los datos actulizados devueltos por ajaxs 
                        //alert("exito es "+respuesta.resultados)
                        let resultados = respuesta.resultados;
                        //alert("Subtotal: " + resultados.subtotal);
                        //alert("Cantidad Final: " + resultados.cantidadFinal);
                        //alert("IVA: " + resultados.iva);
                        //alert("Total: " + resultados.total);
                        
                        subtotal = document.querySelector(".carrito-subtotal");
                        cantidad = document.querySelector(".carrito-cantidad");
                        iva = document.querySelector(".carrito-iva");
                        total = document.querySelector(".carrito-total");


                        subtotal.innerHTML = "Subtotal "+resultados.subtotal
                        cantidad.innerHTML = "Cantidad "+resultados.cantidadFinal
                        iva.innerHTML = "Iva "+resultados.iva
                        total.innerHTML = "Total "+resultados.total



                        stockDisponibleDb = respuesta.stockProducto
                        

                        if (stockDisponibleDb > stockActual){
                            stock_Producto.value = stockDisponibleDb
                            mostrarSmall(small_stock, stockDisponibleDb)
                        }

                    }else if ((respuesta.hasOwnProperty("stockSuperado")) ) {
                        //##### actulizar el input de la clase stock con el nuevo valor disponible  de ese producto 
                        stockDisponible = respuesta.stockSuperado
                        input.value = stockDisponible
                        stock_Producto.value = stockDisponible;
  
                        if (!(small_stock)){
                            
                            console.log("La etiqueta small no se encontró. Creando una nueva etiqueta small.");
                            small_stock = document.createElement("small");
                            // Configurar cualquier otra propiedad del elemento si es necesario
                            let cajaMediana = boton.closest(".carrito-cajaMediana");
                            cajaMediana.querySelector(".carrito-stock").appendChild(small_stock);
                            
                            small_stock.classList.add("smallStock");
                            small_stock.style.color = "red";  
                            small_stock.innerHTML = "stock en línea " + stockDisponible;
                        
                        }
                        
                        
                        mostrarSmall(small_stock, stockDisponible, stockActual )
                        alert(" stock en linea disponible es de : "+stockDisponible)

                        
                    }else{

                        alert("otra cosa ")
                    }

                } else {
                    // Manejar errores aquí

                    alert("fallo ajax por parte del servidor ")
                    //window.location.reload(); 
                
                }
            }
        };

        // Enviar la solicitud con los datos como objeto JSON
        xhr.send(JSON.stringify({ cantidad: cantidad, idCarrito: idCarrito }));
    }

    function mostrarSmall(small_stock, stockDisponible, stockActual ){
        

        console.log("dentre a mostrarSmall ")
        if (small_stock) {

            if (stockDisponible <=20){

                console.log("smallllllllllllllllll definido ")
                small_stock.innerHTML = "stock en linea "+stockDisponible;


            }else if (stockDisponible > 20){
               
                small_stock.parentNode.removeChild(small_stock);
            }
        }

    }

function mostrarMensaje(mensaje){
    window.onload = function() {
        window.setTimeout(function(){
            alert(mensaje);
        },10 ); 
    };
}