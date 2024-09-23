let numeroIntentos = localStorage.getItem("estado")  ?? true; 
const botonReenviar = document.getElementById("botonReenviar");
const span = document.getElementById("mensaje");
let valores = document.querySelectorAll(".valorInput");
let contenidoCentral = document.getElementById("contenido-central-validacionC");
let contenedor = document.getElementById("contenedor-validacionC");

console.log("nInte:"+numeroIntentos);
if (numeroIntentos == "false"){

    console.log("se debio ocultar los elementos. ");
    crearYOcultarElementos();
    eventoBeforeunload();
}else{
    
    setTimeout(() => {
        botonReenviar.style.display = "block";
        botonReenviar.disabled = false;
    }, 10000); //muestra una vez al pasar el minuto.  

}
//implimentar medidas de seguridad desde el serevidor cuando se haga el clic del boton reenviar y lleve un intervalo de 1 minuto para poder enviar la solicitud otra vez. 




function validacion(){

    let resultadoValidacion = validarCampos(valores);

    if(resultadoValidacion){
        let code=""; 
        for (const valor of valores) {
            code+=`${valor.value}`;
        }
        ajax(code);        
    } 
}

function validarCampos(valores){
    
    let contador = 0; 
    for (const valor of valores) {
        
        console.log("value is "+valor.value)

        if ( valor.validity.valueMissing ) {
            
            span.innerHTML="Los campos son requeridos";
            span.style.color = "red";
            contador++;

        }else if(! valor.checkValidity() ) {       
            span.innerHTML="Valor incorrecto";
            span.style.color = "red";
            contador++;
        }
    }
   
    if (contador==0){
        if( span.innerHTML != null || span.innerHTML != undefined ){
            span.innerHTML = ""; 
        }
        return true;
    }
    return false;
}

function ajax(code){

    // Crear objeto XMLHttpRequest
    let xhr = new XMLHttpRequest();

    // Configurar la solicitud
    xhr.open('POST', '/login/crear_cuenta/verificacion_correo', true);
    xhr.setRequestHeader('Content-Type', 'application/json');  // Cambiar el tipo de contenido a JSON
    
    boton = document.getElementById("botonValidar");
    boton.disabled = true;
    boton.style.background = "#f1eeff";
    boton.style.color = "#9a9a9a";

    // Configurar la función de devolución de llamada
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                
                let respuesta = (JSON.parse(xhr.responseText)).estado;
                console.log("respuesta : "+respuesta);
                
                //controlar la respuesta 
                if (respuesta == "ok" ){

                    span.innerHTML = "";
                    alert("Codigo verificado, cuenta registrada. ¡ Ya puedes iniciar sesión ! 🎈 ");
                    window.location.href='/login';
                    
                }else if(respuesta == "falloVerificacion"){

                    span.innerHTML = "codigo incorreto.";
                    span.style.color ="red";

                }else{
                    span.innerHTML = "Vuelve a intentarlo.";
                    span.style.color ="yellow";
                }
            }
        }

        boton.disabled = false
        boton.style.background = "";
        boton.style.color = "black";
    }
    // Enviar la solicitud con los datos como objeto JSON
    xhr.send(JSON.stringify(code));
}  

function agendamiento(){

    console.log("dentre....1");
    botonReenviar.style.display = "none";
    botonReenviar.disabled = true;

    if (numeroIntentos > 0 || numeroIntentos){

        temporizadorReenviar();
        ajaxReenviarCodigo();
        console.log("nIntentos agendamiento : "+numeroIntentos);
    }else{
        crearYOcultarElementos();
        console.log("llegaste a cero intentos, vuelve a intentarlo. ")
        console.log("nIntentos agendamiento : "+numeroIntentos);
    }


}

function temporizadorReenviar(){

    const spanT = document.querySelector('.spanTiempo');
    const p = document.querySelector('.pReenviar');
    let tiempo = 2;

    p.style.display="block"; 
    
    let identificador = setInterval(() => {
        spanT.textContent=` ${tiempo}`;
        if (tiempo == 0){
            p.style.display = "none";
            clearInterval(identificador);
            botonReenviar.style.display = "block";
            botonReenviar.disabled = false;
        }else{
            tiempo--;
        }
    }, 1000);
}


// this a function is for execute the function of reenviar , mirar esta parte. 
function ajaxReenviarCodigo(){

    // Crear objeto XMLHttpRequest
    let xhr = new XMLHttpRequest();

    // Configurar la solicitud
    xhr.open('GET', '/login/crear_cuenta/reenviar_codigo', true);
    xhr.setRequestHeader('Content-Type', 'application/json'); // Cambiar el tipo de contenido a JSON

    // Configurar la función de devolución de llamada
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                
                let respuesta = (JSON.parse(xhr.responseText));
                console.log("respuesta reenviar :"+respuesta);
                
                //controlar la respuesta 
                if (respuesta.estado=="ok" && respuesta.nIntentos !== null && respuesta.nIntentos !== undefined ){
                    numeroIntentos = respuesta.nIntentos;
                    console.log("ajax intentos : "+respuesta.nIntentos);


                }else if(respuesta == "fail"){

                    span.style.color ="yellow";
                    span.innerHTML = "Vuelve a intentarlo.";
                }else{
                    span.style.color ="red";
                    span.innerHTML = "Vuelve a intentarlo."; 
                }
            }
        }
    }
    // Enviar la solicitud 
    xhr.send();
}

function temporizadorTiempoFuera(){
    
    let tiempoAlmacenado = localStorage.getItem("tiempo");
    
    if (tiempoAlmacenado){
        console.log("se ejecuta formatear");
        tiempoAlmacenado = formatearRespuesta(tiempoAlmacenado);
    }

    let tiempoTrascurrido = tiempoAlmacenado || ((2 * 60) + (50)) * 1000; 
    
    let endTime = new Date().getTime() + tiempoTrascurrido;
    $(document).ready(function() {
        $('.p-tiempo-trascurrido').countdown(endTime, function(event) {
            $(this).html(event.strftime('%M : %S segundos'));

            //verificar cuando sea 00. 
            
        });
    });
    
}
function crearYOcultarElementos(){

    contenidoCentral.style.display="none";
    localStorage.setItem("estado", false)
    temporizadorTiempoFuera();

    const nuevoSpan = document.createElement('span'),
    nuevoP = document.createElement('p'),
    nuevoARegresar = document.createElement("a"),
    nuevoAConctanos= document.createElement('a'),
    nuevoBoton = document.createElement('button');
    
   nuevoSpan.textContent = "Excediste el numero de intentos fallidos, vuelve a intentalo en : ";
   nuevoSpan.classList.add("span-tiempo-fuera");
   nuevoP.classList.add("p-tiempo-trascurrido");
   nuevoAConctanos.href = "#";
   nuevoAConctanos.textContent = "Conctatanos";
   nuevoARegresar.href = "/";
   nuevoBoton.textContent = "Regresar"
   nuevoBoton.style.cursor = "pointer";

   contenedor.append(nuevoSpan,nuevoP,nuevoAConctanos,nuevoARegresar);
   nuevoARegresar.appendChild(nuevoBoton);
}

function eventoBeforeunload(){

    window.addEventListener('beforeunload',(event) => {
        console.log("antes de ser cargada. "); 
        $(document).ready(function() {
            let seleccion = document.querySelector(".p-tiempo-trascurrido");
            let cadena = seleccion.textContent;
            console.log(cadena + " cadena ");
            let tiempo = cadena.replace("segundos","").replace(":", "").replace("  ", "").replace(" ", "");
            console.log("tiempo es : "+tiempo);
            localStorage.setItem("tiempo", tiempo);
        });
    });
   
}
function formatearRespuesta(tiempoAlmacenado){
   
    console.log("111111:"+ tiempoAlmacenado);
    console.log("tamano : "+ tiempoAlmacenado.length);
    
    let milisegundos;

    if(tiempoAlmacenado.length == 4){

        let minutos = parseInt(tiempoAlmacenado.substring(0,2), 10); 
        let segundos = parseInt(tiempoAlmacenado.substring(2,4), 10); 

        milisegundos = ((minutos * 60) + (segundos)) * 1000;  

        console.log("minutos : "+ minutos);
        console.log("segundos : "+ segundos);
        console.log("milisegundos : "+ milisegundos);
    }
   
    return milisegundos;
}