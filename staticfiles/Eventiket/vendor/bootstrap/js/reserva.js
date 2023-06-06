// Función para manejar la selección de butacas
function seleccionarButaca(element) {
    if (element.classList.contains("selected")) {
      element.classList.remove("selected");
    } else {
      element.classList.add("selected");
    }
  }
  
  // Obtener el formulario de reserva
  const form = document.querySelector("form");
  
  // Agregar un listener al evento submit del formulario
  form.addEventListener("submit", function (event) {
    // Obtener todas las butacas seleccionadas
    const selectedSeats = document.querySelectorAll(".seat.selected");
  
    // Crear un input oculto por cada butaca seleccionada y agregarlo al formulario
    selectedSeats.forEach(function (seat) {
      const input = document.createElement("input");
      input.setAttribute("type", "hidden");
      input.setAttribute("name", "butacas");
      input.setAttribute("value", seat.value);
      form.appendChild(input);
    });
  
    // Deshabilitar el formulario para evitar envíos múltiples
    form.setAttribute("disabled", true);
  });