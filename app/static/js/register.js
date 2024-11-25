document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evita el envío estándar del formulario

    // Recopila los datos del formulario
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries()); // Convierte FormData a un objeto JSON

    try {
        // Envía los datos en formato JSON al backend
        const response = await fetch('/auth/api/register', { // Asegúrate de que esta ruta sea correcta
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // Convierte el objeto a JSON
        });

        const result = await response.json(); // Procesa la respuesta como JSON

        if (response.ok) {
            alert(result.message || 'Usuario registrado exitosamente.');
            window.location.href = '/auth/information'; // Redirige al login tras un registro exitoso
        } else {
            alert(result.message || 'Error al registrar el usuario.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error en la solicitud.');
    }
});
