import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { validarCodigo } from "../api/users";
import "./LoginPage.css";

export default function LoginPage() {
  const navigate = useNavigate();
  const [codigo, setCodigo] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const { data } = await validarCodigo(codigo);
      localStorage.setItem("user", JSON.stringify(data));
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Código inválido o no registrado.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Sección izquierda: formulario */}
      <div className="login-box">
        <img
          src="https://aula-virtual.unamad.edu.pe/images/themes/unamad/logo.png"
          alt="Logo Universidad"
          className="logo-institucional"
        />
        <h1>Aula Virtual</h1>

        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label htmlFor="codigo">Código de estudiante</label>
            <input
              id="codigo"
              type="text"
              placeholder="Ingrese su código"
              value={codigo}
              onChange={(e) => setCodigo(e.target.value)}
              required
            />
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? "Ingresando..." : "Ingresar"}
          </button>
        </form>

        <div className="info-sections">
          <p>
            <strong>Biblioteca</strong>
          </p>
          <p>
            <strong>Convocatoria Beca Permanencia 2025</strong>
          </p>
        </div>
      </div>

      {/* Sección derecha: imagen difuminada */}
      <div className="login-image"></div>
    </div>
  );
}