Considerar:

Para el Backend:
1. Activar el entorno virtual venv
2. Descargar las librerias del archivo requirements.txt
3. En Visual Studio, a veces no se identifica las bibliotecas, esto es porque debemos definir el intérprete, solo le dan click en la parte inferior y buscan el archiv "python.exe" dentro de la carpeta de venv (O busqquen en internet)
4. Para levantar el backend, deben ejecutar el siguiente comando en la ruta "src, donde está el archivo "main.py"

                uvicorn main:app ---reload

Para el Fronted:
1. Ejecutar el comando "npm run dev" dentro de la carpeta "proyectoia"