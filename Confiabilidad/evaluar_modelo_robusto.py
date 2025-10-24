import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split

# ============================
# 📂 Rutas
# ============================
dataPath = r"D:/PROYECTOS/IA/asistenciaweb/Backend/output/2025-1"
model_path = r"D:/PROYECTOS/IA/asistenciaweb/Backend/facial/modeloLBPHFace.xml"

# ============================
# 🧠 Cargar modelo base
# ============================
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(model_path)

# ============================
# 📸 Cargar dataset
# ============================
imagePaths = os.listdir(dataPath)
faces = []
labels = []
label_names = {}
IMG_SIZE = (200, 200)
current_label = 0

for personName in imagePaths:
    personPath = os.path.join(dataPath, personName)
    if not os.path.isdir(personPath):
        continue
    label_names[current_label] = personName
    for fileName in os.listdir(personPath):
        img_path = os.path.join(personPath, fileName)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img_resized = cv2.resize(img, IMG_SIZE)
        img_resized = cv2.equalizeHist(img_resized)
        faces.append(img_resized)
        labels.append(current_label)
    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

# ============================
# ✂️ Dividir dataset
# ============================
X_train, X_test, y_train, y_test = train_test_split(faces, labels, test_size=0.3, random_state=42)

print(f"📚 Entrenamiento: {len(X_train)} imágenes")
print(f"🧪 Prueba: {len(X_test)} imágenes")

# ============================
# 🔁 Reentrenar con solo X_train
# ============================
print("\n🧠 Reentrenando modelo solo con conjunto de entrenamiento...")
retrained_model = cv2.face.LBPHFaceRecognizer_create()
retrained_model.train(X_train, np.array(y_train))

# ============================
# 🧪 Función de variación artificial
# ============================
def aplicar_variacion(img):
    """Aplica transformaciones leves para probar robustez."""
    # Rotación leve
    angulo = np.random.uniform(-10, 10)
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), angulo, 1)
    img = cv2.warpAffine(img, M, (w, h))

    # Variar brillo y contraste
    alpha = np.random.uniform(0.8, 1.2)  # contraste
    beta = np.random.randint(-20, 20)    # brillo
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # Añadir ruido leve
    noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)

    return img

# ============================
# 📈 Evaluación robusta
# ============================
correctas_normales = 0
correctas_variadas = 0
total = len(X_test)

for i, face in enumerate(X_test):
    label_real = y_test[i]

    # Predicción normal
    label_pred, _ = retrained_model.predict(face)
    if label_pred == label_real:
        correctas_normales += 1

    # Predicción con variación artificial
    face_mod = aplicar_variacion(face)
    label_pred_var, _ = retrained_model.predict(face_mod)
    if label_pred_var == label_real:
        correctas_variadas += 1

precision_normal = (correctas_normales / total) * 100
precision_variada = (correctas_variadas / total) * 100

# ============================
# 📊 Resultados finales
# ============================
print("\n==============================")
print("📊 RESULTADOS DE EVALUACIÓN")
print("==============================")
print(f"✅ Precisión normal: {precision_normal:.2f}%")
print(f"⚡ Precisión con variaciones: {precision_variada:.2f}%")
print(f"📉 Diferencia de robustez: {precision_normal - precision_variada:.2f}%")
print("==============================\n")
