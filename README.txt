Considerar : 

🗄️ Configuración de la Base de Datos

1.-Descarga el script SQL desde la carpeta /database.
2.-Crea una nueva base de datos en MySQL (el nombre no es importante).
3.-Ejecuta el script descargado dentro de esa base de datos.
4.-En la tabla evento_acceso, elimina la columna snapshot (todo lo demás debe permanecer igual).
5.-En el archivo db.py, modifica la variable de contraseña para que coincida con tu usuario de MySQL.
6.-Inserta un registro en la tabla de estudiantes con los siguientes valores:

INSERT INTO estudiante (codigo, nombres, apellidos, dni, correo_institucional, activo)
VALUES ('00000000', 'desconocido', NULL, NULL, NULL, 0);


💻 Configuración del Backend

1.- Crear el entorno virtaul dentro de la carpeta src usando el comando "python -m venv venv"
2.- Activamos este entorno con venv\Scripts\activate
3.- Instalamos las dependencias con el entorno activado usando "pip install -r requirements.txt"
4.- Modificamos las rutas dentro de captura_rostros.py, entrenar_Rostros.py, reconocer_rostros.py y dentro de la carpeta services
los archivos face_routes.py
5.- Iniciamos el entorno con uvicorn main:app --reload

🌐 Configuración del Frontend
1.-Instalamos las dependencias con npm install y npm build
2.-Iniciamos el servidor con npm run dev 