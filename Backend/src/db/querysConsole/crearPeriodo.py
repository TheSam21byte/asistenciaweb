import mysql.connector
from tabulate import tabulate

# 🔹 CONFIGURACIÓN DE CONEXIÓN
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="211221",
    database="dbia"
)
cursor = db.cursor(dictionary=True)

# -------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------
def insertar_periodo(nombre, inicio, fin):
    cursor.execute(
        "INSERT INTO periodo (nombre, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)",
        (nombre, inicio, fin)
    )
    db.commit()
    print(f"✅ Periodo académico {nombre} creado correctamente.")

def obtener_o_crear_docente(nombre, apellido):
    correo = f"{nombre[0].lower()}{apellido.lower().replace(' ', '')}@unamad.edu.pe"
    cursor.execute("SELECT id_docente FROM docente WHERE correo_institucional = %s", (correo,))
    docente = cursor.fetchone()
    if docente:
        return docente["id_docente"], correo
    cursor.execute(
        "INSERT INTO docente (nombres, apellidos, correo_institucional, activo) VALUES (%s, %s, %s, 1)",
        (nombre, apellido, correo)
    )
    db.commit()
    return cursor.lastrowid, correo

def obtener_o_crear_aula(nombre):
    cursor.execute("SELECT id_aula FROM aula WHERE nombre = %s", (nombre,))
    aula = cursor.fetchone()
    if aula:
        return aula["id_aula"]
    ubicacion = "Pabellón B"
    cursor.execute(
        "INSERT INTO aula (nombre, ubicacion) VALUES (%s, %s)",
        (nombre, ubicacion)
    )
    db.commit()
    return cursor.lastrowid

def crear_curso(nombre, codigo, creditos, id_docente):
    cursor.execute(
        "INSERT INTO curso (nombre, codigo, creditos, id_docente) VALUES (%s, %s, %s, %s)",
        (nombre, codigo, creditos, id_docente)
    )
    db.commit()
    return cursor.lastrowid

def relacionar_curso_periodo(id_curso, id_docente, id_periodo):
    cursor.execute(
        "INSERT INTO curso_periodo (id_curso, id_docente, id_periodo) VALUES (%s, %s, %s)",
        (id_curso, id_docente, id_periodo)
    )
    db.commit()

# -------------------------------------------------------------
# BLOQUE PRINCIPAL
# -------------------------------------------------------------
print("===== CREAR NUEVO PERIODO ACADÉMICO =====")

nombre_periodo = input("🧾 Ingrese nombre del periodo (Ej: 2025-1): ")
fecha_inicio = input("📅 Fecha de inicio (YYYY-MM-DD): ")
fecha_fin = input("📅 Fecha de fin (YYYY-MM-DD): ")

insertar_periodo(nombre_periodo, fecha_inicio, fecha_fin)

# Obtener el id del periodo recién creado
cursor.execute("SELECT id_periodo FROM periodo WHERE nombre = %s", (nombre_periodo,))
id_periodo = cursor.fetchone()["id_periodo"]

# -------------------------------------------------------------
# CURSOS
# -------------------------------------------------------------
n = int(input("📚 Ingrese la cantidad de cursos en este periodo: "))

for i in range(1, n + 1):
    print(f"\n➡️ Curso {i} ------------------------------")
    nombre_curso = input("Nombre del curso: ")
    codigo_curso = input("Código del curso (Ej: INF101): ")
    creditos = int(input("Créditos: "))

    print("\n👨‍🏫 Datos del docente asignado:")
    nom_doc = input("  Nombres: ")
    ape_doc = input("  Apellidos: ")

    id_docente, correo_doc = obtener_o_crear_docente(nom_doc, ape_doc)

    print(f"  ✉️ Correo generado automáticamente: {correo_doc}")

    print("\n🏫 Datos del aula asignada:")
    nom_aula = input("  Nombre del aula (Ej: A-302): ")
    id_aula = obtener_o_crear_aula(nom_aula)

    id_curso = crear_curso(nombre_curso, codigo_curso, creditos, id_docente)
    relacionar_curso_periodo(id_curso, id_docente, id_periodo)

    print(f"✅ Curso '{nombre_curso}' asignado a {nom_doc} {ape_doc} en aula {nom_aula} (Pabellón B).\n")

# -------------------------------------------------------------
# RESUMEN FINAL
# -------------------------------------------------------------
cursor.execute("""
SELECT p.nombre AS periodo, c.nombre AS curso, d.nombres AS docente, d.correo_institucional AS correo, a.nombre AS aula, a.ubicacion
FROM curso_periodo cp
JOIN periodo p ON cp.id_periodo = p.id_periodo
JOIN curso c ON cp.id_curso = c.id_curso
JOIN docente d ON cp.id_docente = d.id_docente
WHERE p.id_periodo = %s
""", (id_periodo,))
rows = cursor.fetchall()

print("\n===== RESUMEN DEL PERIODO CREADO =====")
print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))

cursor.close()
db.close()
