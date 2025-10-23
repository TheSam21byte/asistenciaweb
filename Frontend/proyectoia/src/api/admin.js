import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function loginAdmin(codigo, passw) {
  try {
    const response = await axios.post(`${API_URL}/admin/login`, { codigo, passw });
    return {
      data: response.data,
      intentosRestantes: response.headers["x-ratelimit-remaining"] ?? "N/A",
    };
  } catch (error) {
    const status = error.response?.status;
    const mensaje =
      status === 401
        ? "Código o contraseña incorrectos"
        : status === 429
        ? "Demasiados intentos. Espera un momento."
        : "Error de conexión con el servidor";

    throw {
      message: mensaje,
      intentosRestantes: error.response?.headers["x-ratelimit-remaining"] ?? "0",
    };
  }
}

export const obtenerAsistenciaPorCodigo = async (codigo, fecha = null) => {
    // Construir la URL con el código
    let url = `${API_URL}/admin/asistencia/${codigo}`; 

    // Si se proporciona una fecha, añadirla como query parameter
    if (fecha) {
        url += `?fecha=${fecha}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
        // Asume que el backend envía un JSON con el detalle del error
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error al obtener asistencia");
    }

    return response.json();
};