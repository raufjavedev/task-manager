document.addEventListener("DOMContentLoaded", fetchUser);

// Obtener datos del usuario
async function fetchUser() {
    try {
        const response = await fetch("/api/profile");
        const data = await response.json();

        const divUsername = document.getElementById('username');

        divUsername.innerHTML = `
            <span class="flex items-center gap-2 text-gray-300 cursor-pointer px-1 py-2 rounded-lg hover:text-white transition duration-300 active:scale-95">
                <i class="fas fa-user-circle text-xl"></i> 
                ${data.user?.fullname}
            </span>
        `;

        const divDate = document.getElementById('created-at');

        divDate.innerHTML = `
            <p class="text-gray-400">Usuario desde: ${formatRegistrationDate(data.user?.created_at)}</p>
        `;

        document.getElementById('user-id').value = data.user.id;
        document.getElementById('full-name').value = data.user.fullname;
        document.getElementById('username-input').value = data.user.username;
        document.getElementById('email').value = data.user.email;

    } catch (error) {
        console.error("Error al obtener el perfil:", error);
    }
}

// Eliminar al usuario
async function deleteUser() {
    try {
        const userId = document.getElementById('user-id').value;

        console.log(userId);

        // Mostrar confirmación antes de eliminar
        const confirmDelete = window.confirm("Al eliminar tu cuenta, también se eliminarán todas tus tareas asociadas. Esta acción es irreversible. ¿Estás seguro de que deseas continuar?");

        if (!confirmDelete) return;

        const response = await fetch(`/api/user/${userId}`, { method: "DELETE" });

        if (!response.ok) {
            const errorMessage = await response.text();
            throw new Error(errorMessage || "Error al eliminar la cuenta");
        }

        alert("Cuenta eliminada");

        window.location.href = "/login";
    } catch (error) {
        console.error("Error al eliminar la cuenta:", error);
        alert("No se pudo eliminar la cuenta. Intenta de nuevo.");
    }
}

// Actualizar usuario existente
async function updateUser() {
    try {
        const id = document.getElementById('user-id').value;
        const fullName = document.getElementById('full-name').value;
        const username = document.getElementById('username-input').value;
        const email = document.getElementById('email').value;

        const response = await fetch(`/api/user/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fullName, username, email })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message || "Error al actualizar usuario");

        alert(data.message);

        fetchUser();
        document.getElementById('profileModal').classList.add("hidden");
    } catch (error) {
        console.error("Error al actualizar usuario:", error);
    }

}

// Formato ([dia] de [Mes] de [Año])
function formatRegistrationDate(stringDate) {
    const fecha = new Date(stringDate);
    return fecha.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
}

