// document.addEventListener("DOMContentLoaded", fetchTasks);

document.addEventListener("DOMContentLoaded", () => {
    fetchTasks(); // Cargar tareas al inicio
});

// Obtener y mostrar las tareas
async function fetchTasks() {
    try {
        const response = await fetch("/api/tasks");
        const data = await response.json();

        // Contadores separados para cada tabla
        let pendingCounter = 1;
        let inProgressCounter = 1;
        let completedCounter = 1;

        const pendingList = document.getElementById("pending-list");
        const inProgressList = document.getElementById("in-progress-list");
        const completedList = document.getElementById("completed-list");

        // Limpiar las tablas antes de agregar nuevas filas
        pendingList.innerHTML = "";
        inProgressList.innerHTML = "";
        completedList.innerHTML = "";

        data.tasks.forEach(task => {
            const tr = document.createElement("tr");
            tr.className = "border-b border-gray-600 bg-gray-850 hover:bg-gray-700 transition duration-200";

            tr.innerHTML = `
                <td class="p-4 text-gray-300">${getCounter(task.status)}</td>
                <td class="p-4 font-semibold text-gray-100">${task.title}</td>
                <td class="p-4 text-gray-400">${task.description}</td>
                <td class="p-4 text-gray-300">${formatDate(task.due_date)}</td>
                <td class="p-4">
                    <span class="bg-${task.status === 'Pendiente' ? 'orange' : task.status === 'En Progreso' ? 'blue' : 'green'}-500 text-white px-2 py-1 rounded text-xs font-semibold">
                        ${task.status}
                    </span>
                </td>
                <td class="p-4 flex justify-center space-x-4">
                    <button onclick="detail(${task.id})" class="text-gray-400 hover:text-green-500 transition duration-300">
                        <i class="fas fa-eye text-lg"></i>
                    </button>
                    <button onclick="openEditTaskModal(${task.id})" class="text-gray-400 hover:text-blue-500 transition duration-300">
                        <i class="fas fa-edit text-lg"></i>
                    </button>
                    <button onclick="deleteTask(${task.id})" class="text-gray-400 hover:text-red-500 transition duration-300">
                        <i class="fas fa-trash text-lg"></i>
                    </button>
                </td>
            `;

            // Dependiendo del estado, agregamos la tarea a la tabla correspondiente
            if (task.status === "Pendiente") {
                pendingList.appendChild(tr);
            } else if (task.status === "En Progreso") {
                inProgressList.appendChild(tr);
            } else if (task.status === "Completada") {
                completedList.appendChild(tr);
            }
        });

        // Función para manejar el contador de cada tabla
        function getCounter(status) {
            if (status === "Pendiente") {
                return pendingCounter++;
            } else if (status === "En Progreso") {
                return inProgressCounter++;
            } else if (status === "Completada") {
                return completedCounter++;
            }
        }

        // Variables para almacenar los contadores
        let countPending = 0;
        let countInProgress = 0;
        let countCompleted = 0;

        // Recorrer las tareas y contar según el estado
        data.tasks.forEach(task => {
            if (task.status === "Pendiente") countPending++;
            else if (task.status === "En Progreso") countInProgress++;
            else if (task.status === "Completada") countCompleted++;
        });

        // Asignar valores a los contadores en el DOM después de contar
        document.getElementById("count-pending").textContent = countPending;
        document.getElementById("count-in-progress").textContent = countInProgress;
        document.getElementById("count-completed").textContent = countCompleted;

    } catch (error) {
        console.error("Error al obtener tareas:", error);
    }
}

// Crear nueva tarea
async function createTask() {
    try {
        const title = document.getElementById("new-task-title").value;
        const description = document.getElementById("new-task-desc").value;
        const due_date = document.getElementById("new-task-date").value;
        const status = document.getElementById("new-task-status").value;

        const response = await fetch("/api/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description, due_date, status })
        });

        if (!response.ok) throw new Error("Error al crear tarea");

        closeCreateTaskModal();
        fetchTasks();
    } catch (error) {
        console.error("Error al crear tarea:", error);
    }
}

// Abrir modal de edición y cargar datos de la tarea
async function openEditTaskModal(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();

        // Si task es un objeto dentro de otro objeto
        const data = task.task ? task.task : task;

        document.getElementById("edit-task-id").value = data.id;
        document.getElementById("edit-task-title").value = data.title;
        document.getElementById("edit-task-desc").value = data.description;

        const dateObj = new Date(data.due_date);
        document.getElementById("edit-task-date").value = dateObj.toISOString().split("T")[0];
        document.getElementById("edit-task-status").value = data.status;

        document.getElementById("editTaskModal").classList.remove("hidden");
    } catch (error) {
        console.error("Error al cargar tarea:", error);
    }
}

// Guardar cambios al editar una tarea
async function updateTask() {
    try {
        const id = document.getElementById("edit-task-id").value;
        const title = document.getElementById("edit-task-title").value;
        const description = document.getElementById("edit-task-desc").value;
        const due_date = document.getElementById("edit-task-date").value;
        const status = document.getElementById("edit-task-status").value;

        const response = await fetch(`/api/tasks/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description, due_date, status })
        });

        if (!response.ok) throw new Error("Error al actualizar tarea");

        closeEditTaskModal();
        fetchTasks();
    } catch (error) {
        console.error("Error al actualizar tarea:", error);
    }
}

// Eliminar una tarea
async function deleteTask(taskId) {
    try {
        // Mostrar confirmación antes de eliminar
        const confirmDelete = window.confirm("¿Estás seguro de que deseas eliminar esta tarea?");
        if (!confirmDelete) return;

        const response = await fetch(`/api/tasks/${taskId}`, { method: "DELETE" });

        if (!response.ok) {
            const errorMessage = await response.text();
            throw new Error(errorMessage || "Error al eliminar tarea");
        }

        alert("Tarea eliminada correctamente");
        fetchTasks(); // Recargar lista de tareas
    } catch (error) {
        console.error("Error al eliminar tarea:", error);
        alert("No se pudo eliminar la tarea. Intenta de nuevo.");
    }
}

// Detalles de la tarea
async function detail(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();

        // Si task es un objeto dentro de otro objeto
        const data = task.task ? task.task : task;

        const title = document.getElementById('task-title');
        const description = document.getElementById('task-description');
        const date = document.getElementById('task-date');
        const status = document.getElementById('task-status');

        title.innerHTML = `
            <p class="text-lg font-semibold"><i class="fa-solid fa-thumbtack"></i> Título:</p>
            <p class="text-gray-300 bg-gray-800 p-2 rounded-lg">${data.title}</p>
        `;

        description.innerHTML = `
            <p class="text-lg font-semibold"><i class="fa-solid fa-pen"></i> Descripción:</p>
            <p class="text-gray-300 bg-gray-800 p-2 rounded-lg">${data.description} </p>
        `;

        date.innerHTML = `
            <p class="text-lg font-semibold"><i class="fa-solid fa-calendar-days"></i> Fecha Vencimiento:</p>
            <p class="text-gray-300 bg-gray-800 p-2 rounded-lg">${formatDate(data.due_date)}</p>
        `;

        status.innerHTML = `
            <p class="text-lg font-semibold"><i class="fa-solid fa-bolt"></i> Estado:</p>
            <p class="text-${data.status == 'Pendiente' ? 'yellow' : data.status == 'En Progreso' ? 'blue' : 'green'}-400 font-semibold bg-gray-800 p-2 rounded-lg">${data.status}</p>
        `;

        document.getElementById("viewTaskModal").classList.remove("hidden");
    } catch (error) {
        console.error("Error al obtener tareas:", error);
    }
}

// Función para formatear la fecha
function formatDate(dateString) {
    if (!dateString) return "Sin fecha";

    // Convertir la fecha en un objeto Date
    const dateObj = new Date(dateString);

    // Validar si la fecha es válida
    if (isNaN(dateObj.getTime())) {
        console.error("Fecha inválida:", dateString);
        return "Fecha inválida";
    }

    // Extraer día, mes y año
    const day = dateObj.getUTCDate().toString().padStart(2, "0");
    const month = (dateObj.getUTCMonth() + 1).toString().padStart(2, "0"); // Se suma 1 porque los meses van de 0 a 11
    const year = dateObj.getUTCFullYear();

    return `${day}/${month}/${year}`;
}

// Asignar color según el estado
function getStatusColor(status) {
    switch (status) {
        case "Pendiente": return "yellow-400";
        case "En Progreso": return "blue-400";
        case "Completada": return "green-400";
        default: return "gray-400";
    }
}

// Funciones para abrir y cerrar los modals
function openModal(modalId) {
    document.getElementById(modalId).classList.remove("hidden");
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add("hidden");
}

function closeEditTaskModal() {
    document.getElementById('editTaskModal').classList.add("hidden");
}

function closeCreateTaskModal() {
    document.getElementById("createTaskModal").classList.add("hidden");
    document.getElementById("new-task-title").value = "";
    document.getElementById("new-task-desc").value = "";
    document.getElementById("new-task-date").value = "";
    document.getElementById("new-task-status").value = "Pendiente";
}
