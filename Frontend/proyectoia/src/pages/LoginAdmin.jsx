// src/components/LoginAdmin.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginAdmin } from "../api/admin";
import "./LoginAdmin.css";

export default function LoginAdmin() {
  const [codigo, setCodigo] = useState("");
  const [passw, setPassw] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // ✅ Llamamos correctamente al backend
      const res = await loginAdmin(codigo, passw);

      // ✅ Verificamos si la respuesta fue exitosa
      if (res.data.status === "ok") {
        // Guardamos el código del admin y redirigimos
        navigate("/monitoreo", { state: { codigo: res.data.codigo } });
      } else {
        setError("Error al iniciar sesión");
      }
    } catch (err) {
      setError(err.message || "Error de conexión con el servidor");
    }
  };

  return (
    <div className="login-container">
      <div className="login-panel">
        <h1>Panel de Administración</h1>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Código"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={passw}
            onChange={(e) => setPassw(e.target.value)}
            required
          />
          <button type="submit">Iniciar sesión</button>
          {error && <p className="error-msg">{error}</p>}
        </form>
      </div>
    </div>
  );
}

