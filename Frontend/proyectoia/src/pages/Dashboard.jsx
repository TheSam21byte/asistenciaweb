import React, { useRef, useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const videoRef = useRef(null);
  const [status, setStatus] = useState("idle"); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState("Pulsa el botón para comenzar el registro.");

  const registrarRostro = async () => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user || !user.codigo) {
      setMessage("Debe iniciar sesión antes de registrar el rostro.");
      setStatus("error");
      return;
    }

    setStatus("loading");
    setMessage("Iniciando captura... Por favor, mira fijamente a la cámara.");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/registrar-rostro/${user.codigo}`,
        { method: "POST" }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      const data = await response.json();
      setStatus("success");
      setMessage(
        data.message || "✅ ¡Rostro registrado correctamente! Ya puedes marcar asistencia."
      );
    } catch (error) {
      console.error("❌ Error al registrar el rostro:", error);
      setStatus("error");
      setMessage("❌ Error: Código no encontrado o problema con la cámara/servidor.");
    }
  };

  // === Datos del usuario ===
  const user = JSON.parse(localStorage.getItem("user"));
  const nombreCompleto = user
    ? `${user.nombres ?? ""} ${user.apellidos ?? ""}`.trim()
    : "Estudiante UNAMAD";
  const primerNombre = nombreCompleto.split(" ")[0] || "Usuario";

  return (
    <div className="dashboard-layout">
      {/* === Panel lateral izquierdo === */}
      <aside className="dashboard-panel">
        <div className="panel-header">
          <img
            src="https://enchufate.pe/wp-content/uploads/2024/04/Marca03-1.png"
            alt="Logo UNAMAD"
            className="panel-logo"
          />
          <h2>Panel Estudiantil</h2>
        </div>

        <ul className="panel-list">
          <li className="highlight-item">
            <strong>Estudiante:</strong> {nombreCompleto}
          </li>
          <li>
            <strong>Asistencia:</strong>{" "}
            <strong className="status-active">Activa</strong>
          </li>
          <li>
            <strong>Próxima clase:</strong> 3:00 PM — INGENIERIA ECONOMICA
          </li>
          <li>
            <strong>Notificaciones:</strong>{" "}
            <strong className="status-alert">2 nuevas</strong>
          </li>
          <li>
            <strong>Docente:</strong> Elena Limones
          </li>
        </ul>
      </aside>

      {/* === Sección principal (derecha) === */}
      <div className="dashboard-main">
        <header className="dashboard-header">
          <h1>Bienvenido, {primerNombre} 👋</h1>
          <p>Sistema de Asistencia Facial — Aula Virtual UNAMAD</p>
        </header>

        <main className="dashboard-content">
          <section className={`dashboard-card status-${status}`}>
            <p className="card-instruction">{message}</p>

            <button
              onClick={registrarRostro}
              className="camera-button"
              disabled={status === "loading"}
            >
              {status === "loading"
                ? "Cargando rostro..."
                : "📸 Registrar rostro"}
            </button>

            <div className="video-container">
              <video
                ref={videoRef}
                width="480"
                height="360"
                autoPlay
                muted
                style={{
                  display:
                    status === "loading" || status === "idle"
                      ? "none"
                      : "block",
                }}
              ></video>

              {(status === "loading" || status === "idle") && (
                <div className="video-placeholder">Cámara inactiva</div>
              )}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
