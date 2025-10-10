import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function validarCodigo(codigo) {
  try {
    const response = await axios.post(`${API_URL}/validar`, { codigo });

    return {
      data: response.data,
      intentosRestantes: response.headers["x-ratelimit-remaining"],
    };
  } catch (error) {
    const status = error.response?.status;
    const mensaje =
      status === 401
        ? "Código inválido o estudiante inactivo"
        : status === 429
        ? "Demasiados intentos. Espera un momento."
        : "Error de conexión con el servidor";

    throw {
      message: mensaje,
      intentosRestantes:
        error.response?.headers["x-ratelimit-remaining"] ?? "0",
    };
  }
}
