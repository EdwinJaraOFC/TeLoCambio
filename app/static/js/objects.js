async function deleteObject(objectId, event) {
    event.preventDefault(); // Detener el comportamiento predeterminado del enlace

    const confirmed = confirm('¿Estás seguro de que deseas eliminar este objeto?');
    if (!confirmed) return;

    try {
        const response = await fetch(`/objects/api/objects/${objectId}`, {
            method: 'DELETE',
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message || 'Objeto eliminado exitosamente.');
            location.reload(); // Recargar la página
        } else {
            alert(result.message || 'No se pudo eliminar el objeto.');
        }
    } catch (error) {
        console.error('Error al intentar eliminar el objeto:', error);
        alert('Ocurrió un error al intentar eliminar el objeto.');
    }
}