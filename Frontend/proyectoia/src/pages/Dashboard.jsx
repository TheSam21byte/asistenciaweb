import React, { useRef } from "react";
import "./Dashboard.css";

function Dashboard() {
  const videoRef = useRef(null);

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error("Error al abrir la cámara:", error);
      alert("No se pudo acceder a la cámara. Asegúrate de permitir el acceso.");
    }
  };

  // 🔹 Obtener datos del estudiante almacenados tras el login
  const user = JSON.parse(localStorage.getItem("user"));

  // 🔹 Generar nombre completo (manejo de nulls por seguridad)
  const nombreCompleto = user
    ? `${user.nombres ?? ""} ${user.apellidos ?? ""}`.trim()
    : "Usuario";

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

          <button onClick={openCamera} className="camera-button">
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
