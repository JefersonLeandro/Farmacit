let numeroIntentos = localStorage.getItem("estado")  ?? true; 
const botonReenviar = document.getElementById("botonReenviar");
const span = document.getElementById("mensaje-vc");
let valores = document.querySelectorAll(".cajaInput-vc");
let contenidoCentral = document.getElementById("contenido-central-validacionC");
let contenedor = document.getElementById("contenedor-validacionC");

if (numeroIntentos == "false"){
    crearYOcultarElementos();
    agregarEventoBeforeunload();
}else{
    
    setTimeout(() => {
        botonReenviar.style.display = "block";
        botonReenviar.disabled = false;
    }, 30000);  

} 

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
                
                //controlar la respuesta 
                if (respuesta == "ok" ){
                    span.innerHTML = "";
                    alert("Codigo verificado, cuenta registrada. ¡ Ya puedes iniciar sesión ! 🎈 ");
                    window.location.href='/login';
                    
                }else if(respuesta == "falloVerificacion"){

                    span.innerHTML = "Codigo incorreto.";
                    span.style.color ="red";

                }else{
                    span.innerHTML = "Vuelve a intentarlo.";
                    span.style.color ="yellow";
                }
            }
        }

        boton.disabled = false
        boton.style.background = "";
        boton.style.color = "white"
       
    }
    // Enviar la solicitud con los datos como objeto JSON
    xhr.send(JSON.stringify(code));
}  

function agendamiento(){

    botonReenviar.disabled = true;
    botonReenviar.style.display = "none";

    if (numeroIntentos > 0 || numeroIntentos){
        temporizadorReenviar();
        ajaxReenviarCodigo();
    }else{
        crearYOcultarElementos();
        agregarEventoBeforeunload();
    }
}

function temporizadorReenviar(){

    const spanT = document.querySelector('.spanTiempo');
    const p = document.querySelector('.pReenviar');
    let tiempo = 59;

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

                console.log("respuesta"+respuesta);

                //controlar la respuesta 
                if (respuesta.estado=="ok" && respuesta.nIntentos !== null && respuesta.nIntentos !== undefined ){
                    numeroIntentos = respuesta.nIntentos;
                    console.log("intentos : ", numeroIntentos);

                }else if(respuesta.estado == "fallo"){

                    span.style.color ="yellow";
                    span.innerHTML = "Vuelve a intentarlo.";
                }else{
                    console.log("fallo : ", respuesta.error);
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
        tiempoAlmacenado = formatearRespuesta(tiempoAlmacenado);
    }
    // calcular tiempo en milisegundos ((2 * 60) + (50)) * 1000 
    let tiempoTrascurrido = tiempoAlmacenado || 170000;
    
    let endTime = new Date().getTime() + tiempoTrascurrido;
    $(document).ready(function() {
        $('.p-tiempo-trascurrido').countdown(endTime, function(event) {
            $(this).html(event.strftime('%M : %S segundos'));
             
            if(event.strftime('%M%S') == "0002"){
                removerEventoBeforeunload();
                localStorage.clear();
                ajaxReinicio();
            } 
        });
    });
    
}
function crearYOcultarElementos(){

    contenidoCentral.style.display="none";
    localStorage.setItem("estado", false);

    temporizadorTiempoFuera();

    const nuevoSpan = document.createElement('span'),
    divMensajeTiempo = document.createElement('div'),
    nuevoP = document.createElement('p'),
    divRegresar = document.createElement('div'),
    nuevoARegresar = document.createElement('a'),
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

    divMensajeTiempo.classList.add("flex-center-center");
    divRegresar.classList.add("flex-center-space-between");

    contenedor.append(divMensajeTiempo,divRegresar);
    divMensajeTiempo.append(nuevoSpan,nuevoP);
    divRegresar.append(nuevoAConctanos,nuevoARegresar);
    nuevoARegresar.appendChild(nuevoBoton);
}

function agregarEventoBeforeunload(){
    window.addEventListener('beforeunload', eventoBu ); 
}

function eventoBu(evento){

    console.log(`type: ${evento.type}`);

    $(document).ready(function() {
        let seleccion = document.querySelector(".p-tiempo-trascurrido");
        let cadena = seleccion.textContent;
        let tiempo = cadena.replace(/\D/g, ''); 
        localStorage.setItem("tiempo", tiempo);
    });

}

function removerEventoBeforeunload(){
    window.removeEventListener("beforeunload", eventoBu);
}


function formatearRespuesta(tiempoAlmacenado){

    let milisegundos;

    if(tiempoAlmacenado.length == 4){ 
        let minutos = parseInt(tiempoAlmacenado.substring(0,2), 10); 
        let segundos = parseInt(tiempoAlmacenado.substring(2,4), 10);
        milisegundos = ((minutos * 60) + (segundos)) * 1000;
    }
    return milisegundos;
}
function ajaxReinicio(){
     
      // Crear objeto XMLHttpRequest
      let xhr = new XMLHttpRequest();

      // Configurar la solicitud
      xhr.open('POST', '/login/crear_cuenta/reiniciar_estado', true);
      xhr.setRequestHeader('Content-Type', 'application/json'); // Cambiar el tipo de contenido a JSON
      // Configurar la función de devolución de llamada
      xhr.onreadystatechange = function () {
          if (xhr.readyState == 4) {
              if (xhr.status == 204 || xhr.status == 200) {
                
                //controlar la respuesta 
                if((xhr.responseText) != ""){
                    let respuesta = (JSON.parse(xhr.responseText));
                    console.log("respuesta: "+respuesta.error);
                }
                
                try {
                    window.location.reload();
                } catch (error) {
                    console.error("el error es : "+error);
                    window.location.reload();
                }
              }
          }
      }
      // Enviar la solicitud 
      xhr.send();

}