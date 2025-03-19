document.addEventListener("DOMContentLoaded", function () {
    const toggleForm = document.getElementById('toggle-form');
    const toggleText = document.getElementById('toggle-text');
    const formTitle = document.getElementById('form-title');
    const nameField = document.getElementById('name-field');
    const emailField = document.getElementById('email-field');
    const submitBtn = document.getElementById('submit-btn');
    const authForm = document.getElementById('authForm');

    let isLogin = true;

    // Asegurar que el botón tenga el atributo data-action al iniciar
    submitBtn.setAttribute("data-action", "login");

    toggleForm.addEventListener('click', function (e) {
        e.preventDefault();

        isLogin = !isLogin;

        if (isLogin) {
            formTitle.innerText = "Iniciar Sesión";
            emailField.classList.add('hidden');  // Ocultar email
            nameField.classList.remove('hidden');  // Mostrar nombre
            submitBtn.innerText = "Ingresar";
            submitBtn.setAttribute("data-action", "login");
            toggleText.innerText = "¿No tienes cuenta?";
            toggleForm.innerText = "Regístrate aquí";
            toggleForm.classList.replace("text-green-400", "text-blue-400");

            clearFields();
        } else {
            formTitle.innerText = "Registro";
            emailField.classList.remove('hidden');  // Mostrar email
            nameField.classList.remove('hidden');  // Ocultar nombre
            submitBtn.innerText = "Registrarse";
            submitBtn.setAttribute("data-action", "register");
            toggleText.innerText = "¿Ya tienes cuenta?";
            toggleForm.innerText = "Inicia sesión";
            toggleForm.classList.replace("text-blue-400", "text-green-400");

            clearFields();
        }
    });

    // Manejo del formulario
    authForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        let action = submitBtn.getAttribute("data-action");
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        let email = null;

        if (action === "register") {
            email = document.getElementById("email").value;
        }

        let url, body;
        if (action === "login") {
            url = "/api/login";
            body = JSON.stringify({ username, password });
        } else {
            url = "/api/register";
            body = JSON.stringify({ username, password, email });
        }

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: body
            });

            const data = await response.json();

            if (data.success) {
                if (action === "login") {
                    localStorage.setItem("token", data.token);
                    window.location.href = "/";
                } else {
                    alert("Usuario registrado con éxito. Ahora inicia sesión.");
                    window.location.href = "/login";
                }
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert("Hubo un error en la solicitud: " + error.message);
        }
    });
});

// Función de logout
function logout() {
    if (confirm("¿Cerrar sesión?")) {
        localStorage.removeItem("token");
        window.location.href = "/logout";
    }
}

// Fncion para limpiar los campos
function clearFields() {
    document.getElementById('username').value = "";
    document.getElementById('email').value = "";
    document.getElementById('password').value = "";
}
