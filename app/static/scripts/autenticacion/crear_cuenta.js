function cambiarColor(){
    
    //nombre
    
        const colorOriginal = "rgb(118, 118, 118)";
        const inputs = document.querySelector(".nombreC");

       inputs.addEventListener("input", function(event) {
           inputs.style.borderBottomColor = "Black";
        });

//                                     Agrega un evento de blur al input
        inputs.addEventListener("blur", function() {
//                                       Cambia el color del input al original  
            inputs.style.borderBottomColor = colorOriginal;  
//                                                                         
       });
       
      //apellido
//                                  
        let inputApellido = document.querySelector(".apellidoC");

      
         inputApellido.addEventListener("input", function(event) {
//                                     
           inputApellido.style.borderBottomColor = "Black";

        });
        
        
        inputApellido.addEventListener("blur", function() {
            inputApellido.style.borderBottomColor = colorOriginal;  
      
       });
       
      //identificacion
      
      let inputDocumento = document.querySelector(".documentoC");
 
        inputDocumento.addEventListener("input", function(event) {
           inputDocumento.style.borderBottomColor = "Black";

        });

//                                
        inputDocumento.addEventListener("blur", function() { 
            inputDocumento.style.borderBottomColor = colorOriginal;  
       });
       
       
       //correo
       
      let inputEmail = document.querySelector(".emailC");
 
        inputEmail.addEventListener("input", function(event) {
           inputEmail.style.borderBottomColor = "Black";

        });

        inputEmail.addEventListener("blur", function() { 
            inputEmail.style.borderBottomColor = colorOriginal;  
       });
       
       
       //Telefono
       
      let inputTelefono = document.querySelector(".telefonoC");
 
      
      
        inputTelefono.addEventListener("input", function(event) {
           inputTelefono.style.borderBottomColor = "Black";

        });

        inputTelefono.addEventListener("blur", function() { 
            inputTelefono.style.borderBottomColor = colorOriginal;  
       });
       
       
       //Contrasena
       
       
      let inputContrasena = document.querySelector(".contraC");
 
        inputContrasena.addEventListener("input", function(event) {
           inputContrasena.style.borderBottomColor = "Black";

        });

        inputContrasena.addEventListener("blur", function() { 
            inputContrasena.style.borderBottomColor = colorOriginal;  
       });
       
       
       //confirmar Contrasena
       
       
      let inputConfirmarC = document.querySelector(".contraCC");
      
        inputConfirmarC.addEventListener("input", function(event) {
           inputConfirmarC.style.borderBottomColor = "Black";

        });

        inputConfirmarC.addEventListener("blur", function() { 
            inputConfirmarC.style.borderBottomColor = colorOriginal;  
       });    
}