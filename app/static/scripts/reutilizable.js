function mostrarAlerta(mensaje){
    // Función para mostrar una alerta después de cargar completamente la página
    window.onload = function() {
        window.setTimeout(function(){
            alert(mensaje);
        }, 500); 
    };
}

function activar(classContenedor, classAtributos){
    const contenedor = document.querySelector(`.${classContenedor}`);
    contenedor.addEventListener('scroll', function() {
        
        let atributos = document.querySelectorAll(".flechasProductos");
        
        atributos.forEach(atributo => {
            atributo.style.display = 'block'
        });
    }, { once: true });
}