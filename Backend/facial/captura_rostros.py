import cv2
import os
import imutils
import sys
import hashlib
import mysql.connector
import subprocess
import numpy as np
from datetime import datetime

# ==============================================
# 🔧 Conexión a base de datos
# ==============================================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dbia"
    )

# ==============================================
# 📂 Rutas y configuración
# ==============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataPath = os.path.join(BASE_DIR, "output", "2025-1")
MAX_FOTOS = 150

# ==============================================
# 🧍‍♂️ Código del estudiante
# ==============================================
if len(sys.argv) > 1:
    codigo_estudiante = sys.argv[1]
else:
    print("⚠️ No se recibió código de estudiante. Se usará 'desconocido'.")
    codigo_estudiante = "desconocido"

personPath = os.path.join(dataPath, codigo_estudiante)
os.makedirs(personPath, exist_ok=True)

print(f"📁 Carpeta lista para el dataset: {personPath}")

# ==============================================
# 🎥 Iniciar cámara
# ==============================================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("❌ ERROR: No se pudo acceder a la cámara.")
    sys.exit()

# ==============================================
# 🤖 Clasificador y detección de rostros
# ==============================================
faceClassif = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ==============================================
# 🧠 Variables de control
# ==============================================
count = 0
hash_md5 = hashlib.md5()
capturas_validas = 0
ult_centro = None  # Para verificar estabilidad del rostro

print(f"\n📸 Iniciando captura precisa de {MAX_FOTOS} imágenes para {codigo_estudiante}...\n")
print("👉 Mantén tu rostro centrado y estable frente a la cámara.")

# ==============================================
# 🔁 Bucle principal de captura
# ==============================================
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ No se pudo leer el frame de la cámara.")
        break

    frame = imutils.resize(frame, width=900)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detección de rostros con mayor precisión
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=1.05,   # más sensible
        minNeighbors=6,     # menos falsos positivos
        minSize=(100, 100)
    )

    auxFrame = frame.copy()

    for (x, y, w, h) in faces:
        # Filtrar rostros que no estén centrados o que cambien mucho de posición
        centro_actual = (x + w // 2, y + h // 2)
        if ult_centro:
            dist = np.linalg.norm(np.array(centro_actual) - np.array(ult_centro))
            if dist > 40:  # el rostro se movió mucho, no capturar
                cv2.putText(frame, "⚠️ Mueve menos tu rostro", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                ult_centro = centro_actual
                continue
        ult_centro = centro_actual

        # Dibujar marco
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (200, 200), interpolation=cv2.INTER_CUBIC)

        # Validar iluminación: evitar capturas muy oscuras
        brillo = np.mean(cv2.cvtColor(rostro, cv2.COLOR_BGR2HSV)[:, :, 2])
        if brillo < 60:
            cv2.putText(frame, "⚠️ Iluminación insuficiente", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            continue

        # Guardar imagen
        nombre_archivo = f'rostro_{count}.jpg'
        ruta_completa = os.path.join(personPath, nombre_archivo)
        cv2.imwrite(ruta_completa, rostro)

        # Generar hash
        with open(ruta_completa, "rb") as f:
            hash_md5.update(f.read())

        count += 1
        capturas_validas += 1

        cv2.putText(frame, f"Captura: {count}/{MAX_FOTOS}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Esperar un momento para evitar fotos repetidas iguales
        cv2.waitKey(80)

    cv2.imshow('📷 Capturando Rostros', frame)

    k = cv2.waitKey(1)
    if k == 27 or count >= MAX_FOTOS:
        break

# ==============================================
# 🧹 Limpieza
# ==============================================
cap.release()
cv2.destroyAllWindows()

print(f"\n💾 Guardando registro ({capturas_validas} imágenes válidas) en la base de datos...")

# ==============================================
# 🗄️ Registrar en base de datos
# ==============================================
conn = None
try:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id_estudiante FROM estudiante WHERE codigo = %s", (codigo_estudiante,))
    estudiante = cur.fetchone()

    if not estudiante:
        print("⚠️ No se encontró el estudiante en la base de datos.")
    else:
        id_estudiante = estudiante["id_estudiante"]
        id_periodo = 1
        path_relativo = personPath
        ts_captura = datetime.now()
        calidad = 0.99
        hash_archivo = hash_md5.hexdigest()
        activo = 1

        sql = """
        INSERT INTO rostro (id_estudiante, id_periodo, path_relativo, ts_captura, calidad, hash_archivo, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (id_estudiante, id_periodo, path_relativo, ts_captura, calidad, hash_archivo, activo)
        cur.execute(sql, values)
        conn.commit()

        print(f"✅ Registro insertado correctamente para {codigo_estudiante}")
        print(f"📂 Carpeta: {path_relativo}")
        print(f"🔑 Hash MD5: {hash_archivo}")

except Exception as e:
    print("❌ Error al registrar en la base de datos:", e)
finally:
    if conn and conn.is_connected():
        cur.close()
        conn.close()

# ==============================================
# 🧠 Entrenamiento automático
# ==============================================
try:
    print("\n🧠 Iniciando entrenamiento automático...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_entrenar = os.path.join(base_dir, "entrenar_rostros.py")

    subprocess.run([sys.executable, script_entrenar], check=True)
    print("✅ Entrenamiento completado exitosamente.")
except subprocess.CalledProcessError as e:
    print("❌ Error durante la ejecución del entrenamiento:", e)
except Exception as e:
    print("❌ Error general al entrenar el modelo:", e)

print(f"\n🎉 ¡Captura finalizada! Se guardaron {capturas_validas} imágenes válidas en: {personPath}")
