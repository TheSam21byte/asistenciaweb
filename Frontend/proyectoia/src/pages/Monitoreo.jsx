import { useState } from "react";
// Asegúrate de que esta importación sea correcta
import { obtenerAsistenciaPorCodigo } from "../api/admin"; 
import "./Monitoreo.css";

export default function Monitoreo({ adminCodigo }) {
  const [codigo, setCodigo] = useState("");
  // NUEVO ESTADO para la fecha
  const [fecha, setFecha] = useState(""); 
  const [asistencias, setAsistencias] = useState([]);
  const [error, setError] = useState("");

  const buscarAsistencia = async () => {
    // Comprobar que al menos el código no esté vacío antes de buscar
    if (!codigo) {
        setError("Por favor, ingrese el código del estudiante.");
        setAsistencias([]);
        return;
    }

    try {
      // MODIFICADO: Ahora pasamos el estado 'fecha' a la función de la API
      const data = await obtenerAsistenciaPorCodigo(codigo, fecha); 
      setAsistencias(data.asistencias);
      setError("");
    } catch (err) {
      // El mensaje de error del backend ahora será más descriptivo
      setError(err.message); 
      setAsistencias([]);
    }
  };

  // Función para formatear la fecha (es la misma)
  const formatDateTime = (ts) => {
    // Reemplaza la 'T' con un espacio
    return ts.replace('T', ' ');
  };

  return (
    <div className="monitoreo-container">
      <h1>Bienvenido {adminCodigo}</h1>

      <div className="buscador">
        <input
          type="text"
          placeholder="Código del estudiante"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
        />
        {/* NUEVO CAMPO DE ENTRADA PARA LA FECHA */}
        <input
          type="date"
          placeholder="Seleccionar Fecha"
          value={fecha}
          onChange={(e) => setFecha(e.target.value)}
        />
        {/* FIN NUEVO CAMPO */}
        <button onClick={buscarAsistencia}>Buscar</button>
      </div>

      {error && <p className="error">{error}</p>}

      {asistencias.length > 0 && (
        <div className="tabla-wrapper">
          <table className="tabla-asistencia">
            <thead>
              <tr>
                <th>Fecha y Hora</th>
                <th>Dirección</th>
                <th>Aula</th>
                <th>Periodo</th>
              </tr>
            </thead>
            <tbody>
              {asistencias.map((a) => (
                <tr key={a.id_evento}>
                  <td>{formatDateTime(a.ts)}</td> 
                  <td>{a.direccion}</td>
                  <td>{a.aula}</td>
                  <td>{a.periodo}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}