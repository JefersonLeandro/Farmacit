const clickSvg = document.getElementById("svgTrash"),
ventana = document.querySelector(".cerrarVentanaG"),
svgCerrar = document.getElementById("svgCerrar"),
btnCancelar = document.getElementById("cancelarBtn"),
overLay = document.querySelector(".overLay"),
btnAceptar1 = document.getElementById("aceptarBtn1"),

lista = document.getElementById("listaP"),
iconoLista = document.querySelector(".favoritos-svg-lista"),
liProducto = document.querySelectorAll(".list-group-item"),
listaSvgX = document.querySelector(".favoritos-svg-x"),
listaCompleta = document.querySelector("#favoritos-lista-completa");

//alerta
clickSvg.addEventListener('click', function () {
ventana.classList.add('active');
overLay.classList.add('active');
listaCompleta.classList.add('active');
});

svgCerrar.addEventListener('click', function () {
ventana.classList.remove('active');
overLay.classList.remove('active');
});

btnCancelar.addEventListener('click', function () {

ventana.classList.remove('active');
overLay.classList.remove('active');
});

//lista

iconoLista.addEventListener('click', function () {
lista.classList.add('active');
overLay.classList.add('active');

console.log("click- lista ")
});



liProducto.forEach(function (li) {
li.addEventListener("click", function (event) {
    lista.classList.remove('active');
    overLay.classList.remove('active');
});
});

listaSvgX.addEventListener('click', function () {

lista.classList.remove('active');
overLay.classList.remove('active');
});


function mostrarMensaje(mensaje){
    window.onload = function () {
        window.setTimeout(function () {
            alert(mensaje);
        }, 10);
    };
}