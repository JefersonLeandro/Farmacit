function activar(){
    const contenedor = document.querySelector(".facturas-scroll");
    let bandera = true;

    contenedor.addEventListener('scroll', function() {
        
        let atributos = document.querySelectorAll(".flechasProductos");
        
        atributos.forEach(atributo => {
            atributo.style.display = 'block'
        });
    }, { once: true });
}
function scrollArriba(){
    if (window.scrollY !== 0){
        window.scrollTo(0, 0);
    }
}