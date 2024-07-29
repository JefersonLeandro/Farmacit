
function activar(){
    const contenedor = document.querySelector(".seccionCV");
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