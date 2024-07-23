
function remplazarValor() {

    let mensajeH5 = document.getElementById("datosInvalidos");
  
    if (mensajeH5 !== null ) {
        document.getElementById("datosInvalidos").innerHTML = "";
    }
} 

function mostrarAlerta(mensaje){
    // Función para mostrar una alerta después de cargar completamente la página
    window.onload = function() {
        window.setTimeout(function(){
            alert(mensaje);
        }, 500); 
    };
}

function cambiarColor(){

    const colorOriginal = "rgb(118, 118, 118)";
    let inputCorreo = document.querySelector("#DocumentoCorreo");


    inputCorreo.addEventListener("input", function(event) {
       inputCorreo.style.borderBottomColor = "black";
    });

//Agrega evento de blur al input
    inputCorreo.addEventListener("blur", function() {

        //Cambia el color del input al original  
      inputCorreo.style.borderBottomColor = colorOriginal;  
                                                        
   });

    let inputContrasena = document.querySelector("#contrasena");

    inputContrasena.addEventListener("input", function(event) {
       inputContrasena.style.borderBottomColor = "black";
    });

//Agrega evento de blur al input
    inputContrasena.addEventListener("blur", function() {
//Cambia el color del input al original  
      inputContrasena.style.borderBottomColor = colorOriginal;                                               
   });

}