 var butacasSeleccionadas = [];

 function seleccionarButaca(butaca) {
   if (!butaca.classList.contains('occupied')) {
     butaca.classList.toggle('selected');
     var fila = butaca.getAttribute('data-fila');
     var columna = butaca.getAttribute('data-columna');
     var asiento = {fila: fila, columna: columna};

     var indice = butacasSeleccionadas.findIndex(function(asientoSeleccionado) {
       return asientoSeleccionado.fila === fila && asientoSeleccionado.columna === columna;
     });

     if (butaca.classList.contains('selected')) {
       if (indice === -1) {
         butacasSeleccionadas.push(asiento);
       }
     } else {
       if (indice !== -1) {
         butacasSeleccionadas.splice(indice, 1);
       }
     }

     var butacasSeleccionadasElement = document.getElementById('butacas-seleccionadas');
     butacasSeleccionadasElement.innerHTML = '';

    butacasSeleccionadas.forEach(function(asientoSeleccionado) {
      var p = document.createElement('p');
       p.textContent = 'Butaca seleccionada: Fila ' + asientoSeleccionado.fila + ' - Columna ' + asientoSeleccionado.columna;
       butacasSeleccionadasElement.appendChild(p);
     });
   }
}
