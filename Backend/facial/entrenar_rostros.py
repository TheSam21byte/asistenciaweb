import cv2
import os
import numpy as np

dataPath = r'D:/Proyectos/AsistencIAWeb/Backend/output/2025-1'
peopleList = os.listdir(dataPath)
print('Lista de personas:', peopleList)

labels = []
facesData = []
label = 0

# Recorrer a través de las personas en el directorio y leer las imágenes
for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo las imágenes de:', nameDir)

    for fileName in os.listdir(personPath):
        print('Rostros:', nameDir + '/' + fileName)

        # Cargar las imágenes en escala de grises
        imagePath = os.path.join(personPath, fileName)
        image = cv2.imread(imagePath, 0)  # 0 = escala de grises
        facesData.append(image)
        labels.append(label)

        cv2.waitKey(10)

    label += 1

cv2.destroyAllWindows()

# Ver las etiquetas (opcional)
print('labels:', labels)
print('Número de etiquetas 0:', np.count_nonzero(np.array(labels) == 0))
print('Número de etiquetas 1:', np.count_nonzero(np.array(labels) == 1))

# Métodos para entrenar el reconocedor
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenar el reconocedor con los rostros
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))

# Guardar el modelo obtenido
face_recognizer.write('modeloLBPHFace.xml')
print("Modelo almacenado...")