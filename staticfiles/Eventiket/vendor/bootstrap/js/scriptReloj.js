// Obtenemos la fecha y hora actual
//const API_KEY = 'eba8f2474915372ea2d4a55c7d57e80c'
const footer = document.querySelector('footer');
// Obtener la información del clima actual basado en la ubicación del usuario
function getWeather() {
    // Obtener la ubicación del usuario
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      const apiKey = 'eba8f2474915372ea2d4a55c7d57e80c'; // Reemplazar con tu propia API key
      const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}&lang=es`;
  
      // Realizar la petición a la API de OpenWeatherMap
      fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
          const probabilidadLluvia = data.rain && data.rain["1h"] ? data.rain["1h"] : 0; // Probabilidad de lluvia en el último 1h
          const temp = data.main.temp;
          const description = data.weather[0].description;
          const location = data.name;
          const weatherElement = document.getElementById("weather-container");
          const iconCode = data.weather[0].icon; // Obtener el código del icono del tiempo
          const iconUrl = `https://openweathermap.org/img/wn/${iconCode}.png`; // Crear la URL del icono utilizando el código obtenido
          //const icon = weather.icon;
          //let icon = '';

                // Cambiar el icono en función de la descripción del clima
            //    if (description.includes('cielo claro')) {
            //        icon = 'cieloClaro.png';
            //    } else if (description.includes('nubes')) {
            //        icon = 'nuboso.png';
            /*    } else if (description.includes('lluvia')) {
                    icon = 'lluvia.png';
                }*/

          //weatherElement.innerHTML = `${location} ${temp}°C | ${description} | ${probabilidadLluvia}%`;
          weatherElement.innerHTML = `<div>
                                        <p>${location}</p>
                                        <p>${description} <img src="${iconUrl}" alt="${description}" /></p>
                                        <h2>${temp}°C </h2>
                                        <p>${probabilidadLluvia}% probabilidad de lluvia</p>
                                      </div>`;
        })
        .catch((error) => {
          console.log(error);
          const weatherElement = document.getElementById("weather");
          weatherElement.innerHTML = "No se pudo obtener la información del clima.";
        });
    });
}





  // Función para actualizar la hora y fecha
  function actualizarHora() {
    const date = new Date();
    const year = date.getFullYear();
    const options = { year: "numeric", month: "long", day: "numeric" };
    const dateString = date.toLocaleDateString("es-ES", options);
    const timeString = date.toLocaleTimeString("es-ES");
  
    // Actualizar el contenido del elemento del pie de página
    footer.innerHTML = '&copy; ' + year + ' Eventiket | ' + dateString + ' | ' + timeString;
  }
  
  // Actualizar la hora cada segundo
  setInterval(actualizarHora, 1000);
  
  // Obtener la información del clima al cargar la página
  getWeather();

  // Mostramos el menú desplegable al hacer clic en el botón correspondiente


