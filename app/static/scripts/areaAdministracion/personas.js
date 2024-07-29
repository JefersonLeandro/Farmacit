function activar(){
    const contenedor = document.querySelector(".seccionCVP");
    let bandera = true;

    contenedor.addEventListener('scroll', function() {
        
        let atributos = document.querySelectorAll(".flechasProductos");
        
        atributos.forEach(atributo => {
            atributo.style.display = 'block'
        });
    }, { once: true });
}
