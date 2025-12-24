// Espera a que todo el contenido del documento esté listo
document.addEventListener("DOMContentLoaded", function() {

  const form = document.getElementById("form-login");

  form.addEventListener("submit", function(event) {
    event.preventDefault(); //Evita el envio automático del formulario

    const correo = form.correo.value.trim();
    const password = form.password.value.trim();

    if (correo === "" || password === "") {
      alert("Por favor, completa todos los campos.");
        return;
    }


    if (password.length < 8) {
      alert("La contraseña debe tener al menos 8 caracteres.");
        return;
    }
    alert("Inicio de sesión exitoso");
    form.reset(); 
    });
    });

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-registro");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); //evita que el formulario se envíe automaticamente

    const nombre = form.nombre.value.trim();
    const correo = form.correo.value.trim();
    const password = form.password.value.trim();

    if (nombre === "") {
      alert("Por favor, ingresa tu nombre.");
      return;
    }

    if (password.length < 8) {
      alert("La contraseña debe tener al menos 8 caracteres.");
      return;
    }

    alert(" Registro exitoso. ¡Bienvenido " + nombre + "!");
    form.reset(); 
     });
    });
// Seleccionamos el formulario
const formularioCompra = document.querySelector("form");

formularioCompra.addEventListener("submit", function(event) {
    event.preventDefault(); // Evita que se recargue la página


    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const libro = document.getElementById("libro").value;
    const direccion = document.getElementById("direccion").value;
    const metodo = document.getElementById("metodo").value;

    if (!nombre || !correo || !libro || !direccion || !metodo) {
        alert("Por favor completa todos los campos.");
        return;
    }

    alert(`¡Compra realizada con éxito!\nLibro: ${libro}\nNombre: ${nombre}\nMétodo de pago: ${metodo}`);

    formularioCompra.reset();
});

const formularioAlquiler = document.querySelector("form");

formularioAlquiler.addEventListener("submit", function(event) {
    event.preventDefault(); 

    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const libro = document.getElementById("libro").value;
    const dias = document.getElementById("dias").value;

    if (!nombre || !correo || !libro || !dias) {
        alert("Por favor completa todos los campos.");
        return;
    }

    const alquileres = JSON.parse(localStorage.getItem("alquileres")) || [];
    alquileres.push({ nombre, correo, libro, dias, fecha: new Date().toLocaleString() });
    localStorage.setItem("alquileres", JSON.stringify(alquileres));

    alert(`¡Alquiler realizado con éxito!\nLibro: ${libro}\nNombre: ${nombre}\nDías de alquiler: ${dias}`);

    formularioAlquiler.reset();
});
