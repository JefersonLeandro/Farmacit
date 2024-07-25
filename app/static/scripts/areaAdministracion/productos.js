const contenedor = document.querySelector(".seccionCV");
let bandera = true;

contenedor.addEventListener('scroll', function() {
    
    let atributos = document.querySelectorAll(".flechasProductos");
    
    atributos.forEach(atributo => {
        atributo.style.display = 'block'
    });
}, { once: true });
