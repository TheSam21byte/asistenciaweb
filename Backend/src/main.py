from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from db.db import get_connection
from models import LoginRequest, EstudianteResponse


# --- Configuración del limitador ---
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="API de Captura Facial UNAMAD")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# --- Manejo de errores personalizado para RateLimitExceeded ---
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    # Maneja compatibilidad entre versiones (reset o reset_in)
    reset_time = getattr(exc, "reset_in", None) or getattr(exc, "reset", 0)

    response = JSONResponse(
        status_code=429,
        content={
            "detail": "Demasiados intentos. Intenta nuevamente en un minuto.",
            "espera_segundos": round(reset_time, 1) if reset_time else None,
        },
    )

    # Headers para frontend y Postman
    response.headers["X-RateLimit-Limit"] = str(exc.limit.limit)
    response.headers["X-RateLimit-Remaining"] = "0"
    if reset_time:
        response.headers["X-RateLimit-Reset"] = str(round(reset_time, 1))

    return response


# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes restringirlo a ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    ],
)


# --- Endpoint principal ---
@app.post("/validar", response_model=EstudianteResponse)
@limiter.limit("3/minute")  # Máximo 3 intentos por minuto
def validar_estudiante(request: Request, data: LoginRequest):
    """
    Valida si un estudiante existe y está activo (simula un login por código).
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute(
            "SELECT * FROM estudiante WHERE codigo=%s AND activo=1",
            (data.codigo,),
        )
        estudiante = cur.fetchone()

        if not estudiante:
            raise HTTPException(
                status_code=401,
                detail="Código inválido o estudiante inactivo"
            )

        # Devuelve como JSONResponse (necesario para SlowAPI)
        return JSONResponse(
            content={
                "id_estudiante": estudiante["id_estudiante"],
                "codigo": estudiante["codigo"],
                "nombres": estudiante["nombres"],
                "apellidos": estudiante["apellidos"],
                "correo_institucional": estudiante["correo_institucional"],
            }
        )

    finally:
        cur.close()
        conn.close()
