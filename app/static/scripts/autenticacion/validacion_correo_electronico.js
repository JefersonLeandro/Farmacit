
const botonReenviar = document.getElementById("botonReenviar");
const span = document.getElementById("mensaje");
let valores = document.querySelectorAll(".valorInput");
let numeroIntentos = 1; 

setTimeout(() => {
    botonReenviar.style.display = "block";
    botonReenviar.disabled = false;
}, 3000); //muestra una vez al pasar el minuto.  


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

    console.log("dentre....");

    if (numeroIntentos > 0 ){

        temporizadorReenviar();
        botonReenviar.style.display = "none";
        botonReenviar.disabled = true;
        ajaxReenviarCodigo();
        console.log("nIntentos agendamiento : "+numeroIntentos);
    }else{
        // volver a activar la varible global que se encuentra en el servidor
        console.log("llegaste a cero intentos, vuelve a intentarlo. ")
        console.log("nIntentos agendamiento : "+numeroIntentos);
    }


}

function temporizadorReenviar(){

    const spanT = document.querySelector('.spanTiempo');
    const p = document.querySelector('.pReenviar');
    let tiempo = 60;

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
                
                let respuesta = (JSON.parse(xhr.responseText)).estado;
                console.log("respuesta reenviar : "+respuesta);
                
                //controlar la respuesta 
                if (respuesta=="ok" && respuesta.nIntentos !== null && respuesta.nIntentos !== undefined ){
                    nIntentos = respuesta.nIntentos;
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
