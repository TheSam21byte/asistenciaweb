import cv2
import os
import winsound
import datetime
import pyautogui
import time
import webbrowser
from urllib.parse import quote_plus  
import requests 

# URL de tu backend FastAPI para registrar el acceso
API_URL = "http://127.0.0.1:8000/api/acceso"  # Ajusta IP y puerto si es necesario
ultimo_registro = {}
COOLDOWN = 10  # segundos

#registrar_evento
def registrar_evento(codigo=None, validado=1, id_aula=1, id_periodo=1, direccion="ENTRA"):
    """
    Envía los datos al endpoint /api/acceso.
    - codigo: código del estudiante, o '00000000' para desconocidos.
    - validado: 1 para estudiante reconocido, 0 para desconocido.
    """
    payload = {
        "codigo": str(codigo) if codigo else "00000000",
        "id_aula": id_aula,
        "id_periodo": id_periodo,
        "validado": validado,
        "direccion": direccion,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[INFO] Evento registrado: {response.json()}")
        else:
            print(f"[ERROR] Falló registro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al backend: {e}")

# =========================
# CONFIGURACIÓN DIRECTORIOS Y MODELO
# =========================
dataPath = r"D:/PROYECTOS/IA/asistenciaweb/Backend/output/2025-1"
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "modeloLBPHFace", "modeloLBPHFace.xml")

imagePaths = os.listdir(dataPath)
print("imagePaths:", imagePaths)

# Crear un reconocedor facial y cargar el modelo previamente entrenado
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(r"D:/PROYECTOS/IA/asistenciaweb/Backend/facial/modeloLBPHFace.xml") 

# Inicializar el clasificador de detección de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                    "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se puede abrir la cámara")

desconocidos = set()

# Directorio para almacenar las imágenes de personas desconocidas
desconocidos_dir = 'Desconocidos'  
if not os.path.exists(desconocidos_dir):
    os.makedirs(desconocidos_dir)

peru_offset = datetime.timedelta(hours=-5)  # Perú tiene UTC-5

# =========================
# BLOQUE WHATSAPP (con cooldown)
# =========================
telefono_peru = "51929370577"  
WA_COOLDOWN_S = 15             
_last_wa_ts = 0.0              

def enviar_whatsapp_alerta(mensaje: str):
    """
    Abre WhatsApp Web con el mensaje prellenado para el número dado.
    Aplica cooldown para evitar múltiples aperturas seguidas.
    """
    global _last_wa_ts
    now = time.time()
    if now - _last_wa_ts < WA_COOLDOWN_S:
        return  # aún en cooldown, no enviar

    msg_encoded = quote_plus(mensaje)
    url = f"https://wa.me/{telefono_peru}?text={msg_encoded}"

    try:
        ok = webbrowser.open(url, new=2)  # intenta abrir en nueva pestaña
        if ok:
            _last_wa_ts = now
            print("Notificación a WhatsApp abierta en el navegador.")
        else:
            print("No se pudo abrir el navegador para WhatsApp.")
    except Exception as e:
        print("Error al abrir WhatsApp:", e)

# =========================
# BLOQUE TELEGRAM (con cooldown)
# =========================

TELEGRAM_TOKEN = os.getenv("TG_BOT_TOKEN", "8271956332:AAExwkK_Pftfrq2SXD92l3SfpODeu57kazU")
CHAT_ID = os.getenv("TG_CHAT_ID", "8157360664")

TG_COOLDOWN_S = 2
_last_tg_ts = 0.0

def enviar_telegram_alerta(mensaje: str):
    """
    Envía mensaje de alerta a Telegram aplicando cooldown.
    """
    global _last_tg_ts
    now = time.time()
    if now - _last_tg_ts < TG_COOLDOWN_S:
        return  # aún en cooldown

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}

    try:
        r = requests.post(url, data=payload, timeout=5)
        if r.status_code == 200:
            _last_tg_ts = now
            print("✅ Notificación enviada a Telegram.")
        else:
            print("⚠️ Error al enviar a Telegram:", r.text)
    except Exception as e:
        print("❌ Error al conectar con Telegram:", e)

# =========================
# FLAGS (por si quieres desactivar/activar canales de alerta)
# =========================
ENVIAR_WHATSAPP = True
ENVIAR_TELEGRAM = True

# =========================
# BUCLE PRINCIPAL DE DETECCIÓN
# =========================
estudiante_reconocido = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aumentar resolución para mayor detalle facial
    frame = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔹 Mejora de contraste y reducción de ruido
    gray = cv2.equalizeHist(gray)               # Corrige diferencias de iluminación
    gray = cv2.GaussianBlur(gray, (5, 5), 0)    # Suaviza el ruido y sombras

    # 🔹 Detector más preciso
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=1.1,     # Sensible a rostros pequeños o lejanos
        minNeighbors=4,      # Requiere coincidencias cercanas (menos falsos positivos)
        minSize=(80, 80)     # Ignora detecciones muy pequeñas
    )
    
    auxFrame = gray.copy()


    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        # Realizar la predicción del rostro
        result = face_recognizer.predict(rostro)

        # Dibujar el rectángulo del rostro detectado y mostrar el resultado
        if result[1] < 70:  # Reconocido
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            codigo = imagePaths[result[0]]
            cv2.putText(frame, f"{codigo} ({result[1]:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # PARA ESTUDIANTE RECONOCIDO
            codigo = imagePaths[result[0]]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{codigo} ({result[1]:.2f})", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            ahora = time.time()
            if codigo not in ultimo_registro or (ahora - ultimo_registro[codigo]) > COOLDOWN:
                print(f"[INFO] Estudiante reconocido: {codigo}")
                registrar_evento(codigo, validado=1)
                ultimo_registro[codigo] = ahora

        else:
            # 🚨 Desconocido
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"Desconocido ({result[1]:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            # PARA ESTUDIANTE DESCONOCIDO
            if (x, y, w, h) not in desconocidos:
                desconocidos.add((x, y, w, h))

                # Obtener la hora actual en la zona horaria de Perú
                current_time = datetime.datetime.now(
                    datetime.timezone(peru_offset)
                ).strftime("%Y-%m-%d_%H-%M-%S")

                # Guardar la imagen del desconocido con la hora
                rostro_save = auxFrame[y:y+h, x:x+w]
                rostro_save = cv2.resize(rostro_save, (200, 200), interpolation=cv2.INTER_CUBIC)
                unknown_image = f"desconocido_{current_time}.jpg"
                cv2.imwrite(os.path.join(desconocidos_dir, unknown_image), rostro_save)

                print(f"[ALERTA] Persona desconocida detectada y guardada: {unknown_image}")

                # Emitir un sonido de alarma
                winsound.Beep(1000, 200)
                registrar_evento(codigo="00000000", validado=0)
                # Enviar alertas (cada una con su propio cooldown)
                #alerta_msg = "🚨 Alerta: Persona Desconocida detectada"
                #if ENVIAR_WHATSAPP:
                #    enviar_whatsapp_alerta(alerta_msg)
                #if ENVIAR_TELEGRAM:
                #    enviar_telegram_alerta(alerta_msg)

    # Mostrar el resultado del reconocimiento
    cv2.imshow('Frame', frame)

    k = cv2.waitKey(1)
    if k == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

log_file = 'detecciones_desconocidas.log'
print("Resumen de personas desconocidas detectadas:")
for idx, (x, y, w, h) in enumerate(desconocidos, start=1):
    log_entry = f"Desconocido {idx}: Coordenadas [x={x}, y={y}, w={w}, h={h}]"
    print(log_entry)
