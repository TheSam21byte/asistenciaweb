import cv2
import os
import imutils
import sys
import hashlib
import mysql.connector
import subprocess

from datetime import datetime

# =================================================================
# CONFIGURACIÓN
# =================================================================

# Conexión a la base de datos MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dbia"
    )

# ✅ Obtener ruta absoluta correcta sin depender del working dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> asistenciaweb/Backend
dataPath = os.path.join(BASE_DIR, "output", "2025-1")
# Cantidad de fotos a capturar
MAX_FOTOS = 150

# =================================================================
# INICIO DE CAPTURA
# =================================================================

if len(sys.argv) > 1:
    codigo_estudiante = sys.argv[1]
else:
    print("⚠️ No se recibió código de estudiante. Se usará 'desconocido'.")
    codigo_estudiante = "desconocido"

personPath = os.path.join(dataPath, codigo_estudiante)

if not os.path.exists(personPath):
    print('📁 Carpeta creada para el dataset: ', personPath)
    os.makedirs(personPath)
else:
    print('📂 La carpeta ya existe. Se añadirán nuevas imágenes.')

# Iniciar cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("❌ ERROR: No se pudo abrir la cámara.")
    exit()

# Clasificador de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    'haarcascade_frontalface_default.xml')

count = 0
hash_md5 = hashlib.md5()

print(f"\n📸 Iniciando captura de {MAX_FOTOS} imágenes para {codigo_estudiante}...\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=800)  # Aumenta el tamaño para más detalle
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔹 Mejora de contraste y reducción de ruido
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=1.1,      # Más sensible a rostros pequeños o lejanos
        minNeighbors=4,       # Requiere 4 detecciones cercanas (reduce falsos positivos)
        minSize=(80, 80)      # Ignora cosas pequeñas que no son rostros
    )

    auxFrame = frame.copy()

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{w}x{h}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 255), 2, cv2.LINE_AA)
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150),
                            interpolation=cv2.INTER_CUBIC)
        nombre_archivo = f'rostro_{count}.jpg'
        ruta_completa = os.path.join(personPath, nombre_archivo)
        cv2.imwrite(ruta_completa, rostro)

        # Actualizar hash con el contenido del archivo
        with open(ruta_completa, "rb") as f:
            hash_md5.update(f.read())

        count += 1
        cv2.putText(frame, f"Capturando: {count}/{MAX_FOTOS}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Capturando Dataset', frame)
    k = cv2.waitKey(1)

    if k == 27 or count >= MAX_FOTOS:
        break

cap.release()
cv2.destroyAllWindows()

# =================================================================
# REGISTRO EN BASE DE DATOS
# =================================================================
print("\n💾 Guardando registro en la base de datos...")

conn = None  # ✅ Previene el NameError si la conexión falla

try:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Buscar id_estudiante según su código
    cur.execute("SELECT id_estudiante FROM estudiante WHERE codigo = %s", (codigo_estudiante,))
    estudiante = cur.fetchone()

    if not estudiante:
        print("⚠️ No se encontró el estudiante en la base de datos.")
    else:
        id_estudiante = estudiante["id_estudiante"]
        id_periodo = 1  # Puedes cambiarlo dinámicamente si lo deseas
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

        print(f"✅ Registro insertado correctamente en la tabla 'rostro' para {codigo_estudiante}.")
        print(f"📂 Carpeta: {path_relativo}")
        print(f"🔑 Hash MD5: {hash_archivo}")

except Exception as e:
    print("❌ Error al registrar en la base de datos:", e)

finally:
    if conn and conn.is_connected():
        cur.close()
        conn.close()

# =================================================================
# ENTRENAR MODELO AUTOMÁTICAMENTE
# =================================================================
try:
    print("\n🧠 Iniciando entrenamiento automático...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_entrenar = os.path.join(base_dir, "entrenar_rostros.py")

    # ✅ Usamos subprocess.run para ejecutar Python correctamente
    subprocess.run([sys.executable, script_entrenar], check=True)
    print("✅ Entrenamiento completado exitosamente.")
except subprocess.CalledProcessError as e:
    print("❌ Error durante la ejecución del script de entrenamiento:", e)
except Exception as e:
    print("❌ Error al entrenar el modelo automáticamente:", e)
# =================================================================
# FIN
# =================================================================
print(f"\n🎉 ¡Captura finalizada! Se guardaron {count} imágenes en: {personPath}")
