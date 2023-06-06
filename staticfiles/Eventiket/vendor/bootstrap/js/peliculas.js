const sesionesBtns = document.querySelectorAll(".sesiones-btn");

sesionesBtns.forEach(function(btn) {
  btn.addEventListener("click", function() {
    const modalId = btn.getAttribute("data-target");
    const modal = document.getElementById(modalId);
    modal.style.display = "block";
    modal.addEventListener("click", function(e) {
      if (e.target.classList.contains("close-btn")) {
        modal.style.display = "none";
      }
    });
  });
});

window.addEventListener("load", function () {
  var modales = document.querySelectorAll(".modal");

  function mostrarSesiones(id) {
    var modal = document.getElementById("modal" + id);
    modal.style.display = "block";
  }

  function ocultarSesiones(id) {
    var modal = document.getElementById("modal" + id);
    modal.style.display = "none";
  }

  for (var i = 0; i < modales.length; i++) {
    var modal = modales[i];
    var botonCerrar = modal.querySelector(".close-btn");
    var id = modal.id.replace("modal", "");

    botonCerrar.addEventListener("click", function () {
      ocultarSesiones(id);
    });

    window.addEventListener("click", function (event) {
      if (event.target == modal) {
        ocultarSesiones(id);
      }
    });
  }
});