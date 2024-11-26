document.getElementById('directionForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Previene el envío predeterminado del formulario

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries()); // Convierte FormData a JSON

    try {
        const response = await fetch('/auth/api/direction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data), // Envía los datos como JSON
        });

        const result = await response.json(); // Procesa la respuesta como JSON

        if (response.ok) {
            alert(result.message || 'Dirección registrada exitosamente.');
            window.location.href = '/auth/hobbies'; // Redirige a hobbies.html tras registro exitoso
        } else {
            alert(result.message || 'Error al registrar la dirección.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error en la solicitud.');
    }
});
