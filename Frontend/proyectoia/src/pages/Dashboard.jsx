import React, { useRef } from "react";
import "./Dashboard.css";

function Dashboard() {
  const videoRef = useRef(null);

  const openCamera = async () => {
  try {
    const user = JSON.parse(localStorage.getItem("user"));
    const codigo = user?.codigo;

    if (!codigo) {
      alert("No se encontró el código del estudiante en sesión.");
      return;
    }

    // 🔹 Llamar al backend para iniciar la captura facial
    const response = await fetch(`http://127.0.0.1:8000/registrar-rostro/${user.codigo}`, {
        method: "POST",
    });

    const data = await response.json();
    alert(data.message || "Captura iniciada correctamente.");

    } catch (error) {
      console.error("Error al registrar rostro:", error);
      alert("No se pudo iniciar la captura facial.");
    }
  };

  // 🔹 Obtener datos del estudiante almacenados tras el login
  const user = JSON.parse(localStorage.getItem("user"));

  // 🔹 Generar nombre completo (manejo de nulls por seguridad)
  const nombreCompleto = user
    ? `${user.nombres ?? ""} ${user.apellidos ?? ""}`.trim()
    : "Usuario";

  // Registra el rostro y manda a la base de datos

  // Registra el rostro y manda a la base de datos
const registrarRostro = async () => {
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user || !user.codigo) {
    alert("Debe iniciar sesión antes de registrar el rostro.");
    return;
  }

  try {
    alert("Se iniciará la captura del rostro. No cierres la cámara.");

    // ✅ Ruta correcta: el backend expone /api/registrar-rostro/{codigo}
    const response = await fetch(`http://127.0.0.1:8000/api/registrar-rostro/${user.codigo}`, {
      method: "POST",
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText);
    }

    const data = await response.json();
    alert(data.message || "¡Rostro registrado correctamente!");
  } catch (error) {
    console.error("❌ Error al registrar el rostro:", error);
    alert("Error al registrar el rostro. Revisa la consola para más detalles.");
  }
};

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Bienvenido, {nombreCompleto || "Usuario"} 👋</h1>
        <p>Sistema de Registro Facial — Proyecto IA</p>
      </header>

      <main className="dashboard-content">
        <section className="dashboard-card">
          <p>
            Aquí puedes registrar tu rostro en nuestra base de datos para el sistema
            de reconocimiento facial.
          </p>

          <button onClick={registrarRostro} className="camera-button">
            📸 Registrar rostro
          </button>

          <div className="video-container">
            <video
              ref={videoRef}
              width="480"
              height="360"
              autoPlay
              onCanPlay={(e) => (e.target.style.display = "block")}
            ></video>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
