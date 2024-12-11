function actualizarFecha(){
    let fecha = new Date().getFullYear(); 
    const seleccion = document.getElementById("fecha");
    seleccion.innerHTML="   "+ fecha +"  "; 
}

function mostrarMensaje(mensaje){
    window.onload = function() {
        window.setTimeout(function(){
            alert(mensaje);
        },10 ); 
    };
}