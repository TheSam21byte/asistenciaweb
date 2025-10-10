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
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Validar Estudiante</h2>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Código de estudiante"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
          />

          {error && <p className="error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Validando..." : "Entrar"}
          </button>
        </form>

        <p className="footer">Proyecto IA — Reconocimiento Facial</p>
      </div>
    </div>
  );
}
