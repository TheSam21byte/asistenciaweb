from fastapi import APIRouter, HTTPException
import subprocess
import sys
import os

router = APIRouter()

@router.post("/registrar-rostro/{codigo}")
def registrar_rostro(codigo: str):
    """
    Lanza el script de captura facial usando el código del estudiante como argumento.
    """
    try:
        # Ruta absoluta al script captura_rostros.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(base_dir, "facial", "captura_rostros.py")

        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail="No se encontró el script de captura.")

        # Ejecutar el script con el código como argumento
        subprocess.Popen([sys.executable, script_path, codigo])

        return {"message": f"Captura facial iniciada para el estudiante {codigo}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tomar-asistencia")
def tomar_asistencia():
    """
    Lanza el script de reconocimiento facial.
    """
    try:
        # Ruta absoluta al script reconocer_rostros.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(base_dir, "facial", "reconocer_rostros.py")

        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail="No se encontró el script de reconocimiento facial.")

        # Ejecutar el script de reconocimiento
        subprocess.Popen([sys.executable, script_path])

        return {"message": "Reconocimiento facial iniciado correctamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
