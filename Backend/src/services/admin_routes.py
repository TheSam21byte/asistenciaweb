from fastapi import APIRouter, HTTPException, Query
from db.db import get_connection
from pydantic import BaseModel

router = APIRouter()

# 📘 Modelo de datos para el login del administrador
class AdminLoginRequest(BaseModel):
    codigo: str
    passw: str


@router.post("/admin/login")
def login_admin(data: AdminLoginRequest):
    """
    Inicia sesión como administrador verificando el código y contraseña en la tabla 'admin'.
    """
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos")

    cursor = conn.cursor(dictionary=True)

    try:
        # 🧠 Asegúrate de que el campo se llame exactamente 'passw' en tu tabla admin
        cursor.execute("SELECT * FROM admin WHERE codigo = %s AND passw = %s", (data.codigo, data.passw))
        admin = cursor.fetchone()

        if not admin:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        return {
            "status": "ok",
            "mensaje": "Inicio de sesión exitoso",
            "codigo": admin["codigo"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------
# RUTA MODIFICADA
# ----------------------------------------------------------------------
@router.get("/admin/asistencia/{codigo}")
def obtener_asistencia(
    codigo: str, 
    fecha: str = Query(None, description="Fecha en formato YYYY-MM-DD") # <-- Parámetro de fecha
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1️⃣ Obtener id_estudiante según su código
        cursor.execute("SELECT id_estudiante FROM estudiante WHERE codigo = %s", (codigo,))
        estudiante = cursor.fetchone()

        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        id_estudiante = estudiante["id_estudiante"]

        # 2️⃣ Construir la consulta SQL dinámicamente
        sql_query = """
            SELECT 
                ea.id_evento,
                ea.ts,
                ea.validado,
                ea.direccion,
                a.nombre AS aula,
                p.nombre AS periodo
            FROM evento_acceso ea
            LEFT JOIN aula a ON ea.id_aula = a.id_aula
            LEFT JOIN periodo p ON ea.id_periodo = p.id_periodo
            WHERE ea.id_estudiante = %s
        """
        sql_params = [id_estudiante]
        
        # 3️⃣ Aplicar el filtro de fecha si se proporciona
        if fecha:
            # Usamos DATE() para comparar solo la parte de la fecha del TIMESTAMP (ts)
            sql_query += " AND DATE(ea.ts) = %s" 
            sql_params.append(fecha)

        # 4️⃣ Ejecutar la consulta
        cursor.execute(sql_query, tuple(sql_params))

        registros = cursor.fetchall()

        if not registros:
            # El mensaje es más específico si se buscó por fecha
            msg = f"No se encontraron registros de asistencia para el código {codigo}"
            if fecha:
                 msg += f" en la fecha {fecha}"
            raise HTTPException(status_code=404, detail=msg)

        return {"codigo": codigo, "asistencias": registros}

    finally:
        cursor.close()
        conn.close()

# ----------------------------------------------------------------------