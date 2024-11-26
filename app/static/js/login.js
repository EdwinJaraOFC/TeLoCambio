document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/auth/api/login', {  // Ruta relativa a la API de login
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Inicio de sesión exitoso.');
            window.location.href = '/dashboard';  // Redirige al dashboard
        } else {
            alert(result.message || 'Error al iniciar sesión.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error en la solicitud.');
    }
});
