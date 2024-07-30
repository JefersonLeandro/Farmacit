

// Seleccionar todos los elementos <li> dentro del contenedor con la id "listaProductos"
let listaItems = document.querySelectorAll("#listaProductos li");
let inputId = document.querySelector("#inputD");

// Iterar sobre cada elemento <li> utilizando forEach
listaItems.forEach(function(li) {
// Agregar un manejador de clic para cada elemento <li>
    li.addEventListener("click", function(event) {
        
        // Obtener el valor del elemento <span> dentro del elemento <li> clicado
        let span = li.querySelector("#unSpan");
    
        inputId.value = span.textContent;
    });
});

