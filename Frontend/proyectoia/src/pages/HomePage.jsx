import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();

  const irAlLogin = () => {
    navigate("/login");
  };

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Bienvenido al sistema de asistencia</h1>

        <button>
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
