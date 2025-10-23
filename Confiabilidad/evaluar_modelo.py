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
# 🧠 Cargar modelo LBPH
# ============================
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(model_path)

# ============================
# 📸 Cargar dataset completo
# ============================
imagePaths = os.listdir(dataPath)
faces = []
labels = []
label_names = {}

current_label = 0
IMG_SIZE = (200, 200)  # Tamaño uniforme para todas las imágenes

for personName in imagePaths:
    personPath = os.path.join(dataPath, personName)
    if not os.path.isdir(personPath):
        continue

    label_names[current_label] = personName
    for fileName in os.listdir(personPath):
        img_path = os.path.join(personPath, fileName)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"⚠️ Imagen no válida: {img_path}")
            continue

        # 🔧 Normalizamos tamaño
        img_resized = cv2.resize(img, IMG_SIZE)

        # 🔍 Ecualizamos histograma para mejorar contraste
        img_resized = cv2.equalizeHist(img_resized)

        faces.append(img_resized)
        labels.append(current_label)

    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

# ============================
# ✂️ Dividir en entrenamiento y prueba
# ============================
X_train, X_test, y_train, y_test = train_test_split(
    faces, labels, test_size=0.2, random_state=42
)

print(f"📚 Datos de entrenamiento: {len(X_train)}")
print(f"🧪 Datos de prueba: {len(X_test)}")

# ============================
# 📈 Evaluar el modelo entrenado
# ============================
correctas = 0
total = len(X_test)
distancias = []

for i, face in enumerate(X_test):
    label_real = y_test[i]
    label_predicho, distancia = face_recognizer.predict(face)
    distancias.append(distancia)

    if label_predicho == label_real:
        correctas += 1

# ============================
# 📊 Resultados finales
# ============================
precision = (correctas / total) * 100
promedio_distancia = np.mean(distancias)
min_dist = np.min(distancias)
max_dist = np.max(distancias)

print("\n==============================")
print("📊 RESULTADOS DE EVALUACIÓN")
print("==============================")
print(f"✅ Precisión del modelo: {precision:.2f}% ({correctas}/{total})")
print(f"🔍 Distancia promedio (confianza inversa): {promedio_distancia:.2f}")
print(f"📉 Distancia mínima: {min_dist:.2f}")
print(f"📈 Distancia máxima: {max_dist:.2f}")
print("==============================\n")

# ✅ Sugerencia interpretativa:
# Distancias menores → mayor similitud / confianza
# Distancias mayores → menor similitud / menos confianza
