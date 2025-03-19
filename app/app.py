from flask import Flask, render_template, redirect, url_for, session
from app.controller.tasks_controller import tasks_bp
from app.controller.users_controller import users_bp
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()  # Cargar las variables de entorno desde .env

app = Flask(__name__)

# Configuración de CORS
CORS(app)

# Configurar la clave secreta desde las variables de entorno
app.secret_key = os.getenv('SECRET_KEY')

# Registrar Blueprints
app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(tasks_bp, url_prefix="/api")

@app.route("/")
def home():
    if "user_id" in session:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
