import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const [codigoEstudiante, setCodigoEstudiante] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  useEffect(() => {
    let stream; // Guardamos el stream para cerrarlo después

    const iniciarCamara = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (error) {
        console.error("❌ Error al acceder a la cámara:", error);
        alert("No se pudo acceder a la cámara. Verifica los permisos del navegador.");
      }
    };

    iniciarCamara();

    // Cleanup: se ejecuta al desmontar el componente
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        if (videoRef.current) videoRef.current.srcObject = null;
      }
    };
  }, []);


  const capturarYEnviarImagen = async () => {
    if (!videoRef.current) return;
    setCargando(true);
    setMensaje("📸 Procesando reconocimiento facial...");
    setCodigoEstudiante(null);

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const imagenBase64 = canvas.toDataURL("image/jpeg");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/reconocer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imagenBase64 }),
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setCodigoEstudiante(data.codigo);
        setMensaje(`✅ ${data.mensaje} (conf: ${data.conf?.toFixed(2) ?? "N/A"})`);
      } else {
        setCodigoEstudiante(null);
        setMensaje(`❌ ${data.mensaje || "No reconocido"}`);
      }
    } catch (error) {
      console.error("Error enviando imagen:", error);
      setMensaje("⚠️ Error de conexión con el servidor");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="home-container">
      <div className="home-header">
        <h1>🎓 Sistema de Asistencia Facial</h1>
        <p>
          ¿Nuevo aquí?{" "}
          <span onClick={() => navigate("/login")} className="registro-link">
            Regístrate
          </span>
        </p>
      </div>

      <div className="panel-reconocimiento">
        <div className="video-box">
          <video ref={videoRef} autoPlay playsInline className="camera-video" />
        </div>

        <button
          className="boton-captura"
          onClick={capturarYEnviarImagen}
          disabled={cargando}
        >
          {cargando ? "Procesando..." : "📷 Tomar asistencia"}
        </button>

        <div className={`resultado ${codigoEstudiante ? "ok" : "fail"}`}>
          {mensaje && <p>{mensaje}</p>}

          {codigoEstudiante && (
            <div className="codigo-box">
              <h3>Código detectado</h3>
              <span>{codigoEstudiante}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
