import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();

  const irAlLogin = () => {
    navigate("/login");
  };

  const tomarAsistencia = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/tomar-asistencia", {
        method: "POST",
      });
      const data = await response.json();
      alert(data.message || "Se inició la toma de asistencia.");
    } catch (error) {
      console.error("Error al tomar asistencia:", error);
      alert("Error al iniciar el reconocimiento facial.");
    }
  };

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Bienvenido al sistema de asistencia</h1>

        <button onClick={tomarAsistencia}>
          Tomar asistencia
        </button>

        <p className="home-register">
          ¿Nuevo aquí?{" "}
          <span onClick={irAlLogin} role="button" tabIndex="0">
            Regístrate
          </span>
        </p>
      </div>
    </div>
  );
}
