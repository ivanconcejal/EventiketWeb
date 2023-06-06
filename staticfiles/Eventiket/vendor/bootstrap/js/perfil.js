
// Obtener el formulario y los campos de usuario y contraseña
const form = document.querySelector('form');
const usernameInput = document.querySelector('input[type="text"]');
const passwordInput = document.querySelector('input[type="password"]');

// Escuchar el evento de envío del formulario
form.addEventListener('submit', (e) => {
  e.preventDefault(); // Evitar el envío del formulario

  const username = usernameInput.value;
  const password = passwordInput.value;

  // Verificar si el usuario y la contraseña coinciden con el superusuario en la base de datos
  if (username === 'ivan' && password === 'IvanConcejal10') {
    // Redirigir al usuario a la página /admin
    window.location.href = '/admin';
  } else {
    // Mostrar un mensaje de error o realizar alguna otra acción si las credenciales no son válidas
    console.log('Credenciales inválidas');
  }
});