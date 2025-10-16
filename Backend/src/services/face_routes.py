from fastapi import APIRouter, HTTPException
import subprocess
import sys
import os
import base64
import numpy as np
import cv2
from datetime import datetime
from fastapi import Request
from db.db import get_connection
from pathlib import Path

router = APIRouter()
conexion = get_connection()
BASE_OUTPUT = Path(__file__).resolve().parent.parent / "output" / "2025-1"

DESCONOCIDOS_DIR = Path(__file__).resolve().parent.parent / "Desconocidos"
DESCONOCIDOS_DIR.mkdir(exist_ok=True)


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

@router.post("/reconocer")
async def reconocer_rostro(request: Request):
    """
    Recibe JSON { "image": "data:image/jpeg;base64,..." }.
    Devuelve { "success": True, "mensaje": "...", "codigo": "<codigo>" }
    o { "success": False, "mensaje": "..." }.
    """
    try:
        data = await request.json()
        image_base64 = data.get("image")
        if not image_base64:
            raise HTTPException(status_code=400, detail="No se envió imagen")

        # Quitar prefijo "data:image/..."
        if "," in image_base64:
            image_base64 = image_base64.split(",", 1)[1]

        image_bytes = base64.b64decode(image_base64)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Rutas según tu estructura
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(current_dir, "facial", "modeloLBPHFace.xml")
        dataPath = os.path.join(current_dir, "output", "2025-1")

        if not os.path.exists(model_path):
            raise HTTPException(status_code=500, detail=f"Modelo no encontrado en {model_path}")
        if not os.path.exists(dataPath):
            raise HTTPException(status_code=500, detail=f"No existe dataPath: {dataPath}")

        imagePaths = sorted(os.listdir(dataPath))

        # Cargar modelo LBPH
        try:
            face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            face_recognizer.read(model_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error cargando modelo LBPH: {e}")

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        if len(faces) == 0:
            return {"success": False, "mensaje": "No se detectó rostro", "codigo": None}

        (x, y, w, h) = faces[0]
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        id_pred, conf = face_recognizer.predict(rostro)

        UMBRAL = 70.0
        if conf < UMBRAL:
            if 0 <= id_pred < len(imagePaths):
                codigo = imagePaths[id_pred]
            else:
                codigo = str(id_pred)

            try:
                conexion = get_connection()
                cursor = conexion.cursor()

                # Obtener id_estudiante a partir del código
                cursor.execute("SELECT id_estudiante FROM estudiante WHERE codigo = %s", (codigo,))
                result = cursor.fetchone()
                if result is None:
                    return {"success": False, "mensaje": f"Estudiante con código {codigo} no encontrado", "codigo": None}

                id_estudiante = result[0]  # Ajusta si usas DictCursor: result['id_estudiante']

                sql = """
                    INSERT INTO evento_acceso (ts, id_estudiante, id_aula, id_periodo, validado, direccion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                ts = datetime.now()
                id_aula = 1
                id_periodo = 1
                validado = 1
                direccion = "ENTRA"

                cursor.execute(sql, (ts, id_estudiante, id_aula, id_periodo, validado, direccion))
                conexion.commit()
                print(f"✅ Evento registrado en BD para estudiante {codigo}")

            except Exception as db_error:
                print(f"⚠️ Error al registrar evento en MySQL: {db_error}")
                return {"success": False, "mensaje": "Error al registrar evento en BD", "codigo": None}

            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conexion' in locals():
                    conexion.close()
            
            # === Determinar curso actual según la hora ===
            hora_actual = datetime.now().hour
            if 15 <= hora_actual < 17:
                curso_actual = "Ingeniería Económica"
            elif 17 <= hora_actual < 19:
                curso_actual = "Redes Neuronales"
            elif 19 <= hora_actual < 21:
                curso_actual = "Inteligencia Artificial"
            else:
                curso_actual = "Fuera de horario académico"
                
            # Aula fija por ahora
            aula_actual = "AV-202ISI"

            return {
                "success": True,
                "mensaje": "Usuario reconocido",
                "codigo": codigo,
                "conf": float(conf),
                "curso": curso_actual,
                "aula": aula_actual
            }

        #DESCONOCIDO 
        
        else:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"desconocido_{timestamp}.jpg"
                save_path = DESCONOCIDOS_DIR / filename
                
                # Recortar y guardar el rostro
                rostro_save = frame[y:y+h, x:x+w]
                rostro_save = cv2.resize(rostro_save, (200, 200), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(str(save_path), rostro_save)

                print(f"[ALERTA] Rostro desconocido guardado en {save_path}")

                # === Registrar evento en la base de datos ===
                try:
                    conexion = get_connection()
                    cursor = conexion.cursor()

                    sql = """
                        INSERT INTO evento_acceso (ts, id_estudiante, id_aula, id_periodo, validado, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    ts = datetime.now()
                    id_estudiante = 5
                    id_aula = 1
                    id_periodo = 1
                    validado = 0  # no validado
                    direccion = "ENTRA"

                    cursor.execute(sql, (ts, id_estudiante, id_aula, id_periodo, validado, direccion))
                    conexion.commit()
                    print(f"⚠️ Evento de persona desconocida registrado en BD ({filename})")

                except Exception as db_error:
                    print(f"❌ Error al registrar evento de desconocido: {db_error}")

                finally:
                    if 'cursor' in locals():
                        cursor.close()
                    if 'conexion' in locals():
                        conexion.close()

            except Exception as e:
                print(f"❌ Error al guardar rostro desconocido: {e}")

            return {
                "success": False,
                "mensaje": "Rostro desconocido (registrado en BD y guardado en carpeta)",
                "codigo": None,
                "conf": float(conf)
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))