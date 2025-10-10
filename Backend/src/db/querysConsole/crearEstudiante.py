import mysql.connector
from tabulate import tabulate
import unicodedata

# ---------- Config DB ----------
CONN = mysql.connector.connect(
    host="localhost",
    user="root",
    password="211221",
    database="dbia",          # <--- usa tu BD real
)
CUR = CONN.cursor(dictionary=True)

def strip_accents(s: str) -> str:
    if not s:
        return s
    nfkd = unicodedata.normalize('NFD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

def generar_correo(nombres: str, apellidos: str) -> str:
    # primera letra del primer nombre + apellidos sin espacios, todo en minúscula, sin tildes
    nombre_1ra = nombres.strip().split()[0][0].lower()
    ap_no_esp = strip_accents(apellidos.replace(' ', '').lower())
    return f"{nombre_1ra}{ap_no_esp}@unamad.edu.pe"

def seleccionar_periodo() -> int:
    CUR.execute("SELECT id_periodo, nombre, fecha_inicio, fecha_fin FROM periodo ORDER BY id_periodo DESC;")
    per = CUR.fetchall()
    if not per:
        raise RuntimeError("No hay periodos en la tabla 'periodo'.")
    print("\n📆 Periodos:")
    print(tabulate(per, headers="keys", tablefmt="fancy_grid"))
    while True:
        try:
            pid = int(input("Ingrese ID del periodo a usar: ").strip())
            CUR.execute("SELECT 1 FROM periodo WHERE id_periodo=%s", (pid,))
            if CUR.fetchone():
                return pid
            print("ID de periodo no válido.")
        except ValueError:
            print("Ingrese un número válido.")

def upsert_estudiante(codigo: str, nombres: str, apellidos: str, dni: str) -> int:
    CUR.execute("SELECT id_estudiante FROM estudiante WHERE codigo=%s", (codigo,))
    row = CUR.fetchone()
    correo = generar_correo(nombres, apellidos)
    if row:
        id_est = row["id_estudiante"]
        # opcional: actualizar datos
        CUR.execute("""
            UPDATE estudiante
            SET nombres=%s, apellidos=%s, dni=%s, correo_institucional=%s, activo=1
            WHERE id_estudiante=%s
        """, (nombres, apellidos, dni, correo, id_est))
        CONN.commit()
        print(f"ℹ️  Estudiante ya existía. Actualizado. (ID {id_est}, correo {correo})")
        return id_est
    CUR.execute("""
        INSERT INTO estudiante (codigo, nombres, apellidos, dni, correo_institucional, activo)
        VALUES (%s,%s,%s,%s,%s,1)
    """, (codigo, nombres, apellidos, dni, correo))
    CONN.commit()
    print(f"✅ Estudiante registrado. Correo: {correo}")
    return CUR.lastrowid

def listar_cursos():
    CUR.execute("""
        SELECT c.id_curso, c.nombre AS curso, c.codigo, c.creditos,
               d.nombres AS docente_nombres, d.apellidos AS docente_apellidos
        FROM curso c
        LEFT JOIN docente d ON c.id_docente = d.id_docente
        ORDER BY c.id_curso;
    """)
    cursos = CUR.fetchall()
    if not cursos:
        raise RuntimeError("No hay cursos en la tabla 'curso'.")
    print("\n📚 Cursos:")
    print(tabulate(cursos, headers="keys", tablefmt="fancy_grid"))
    return [c["id_curso"] for c in cursos]

def listar_aulas():
    CUR.execute("SELECT id_aula, nombre, ubicacion FROM aula ORDER BY id_aula;")
    aulas = CUR.fetchall()
    if not aulas:
        raise RuntimeError("No hay aulas en la tabla 'aula'.")
    print("\n🏫 Aulas:")
    print(tabulate(aulas, headers="keys", tablefmt="fancy_grid"))
    return [a["id_aula"] for a in aulas]

def matricular(id_estudiante: int, id_curso: int, id_aula: int, id_periodo: int):
    # evita duplicados por UNIQUE (id_estudiante,id_curso,id_periodo)
    CUR.execute("""
        SELECT 1 FROM matricula
        WHERE id_estudiante=%s AND id_curso=%s AND id_periodo=%s
    """, (id_estudiante, id_curso, id_periodo))
    if CUR.fetchone():
        print(f"⚠️  Ya estaba matriculado en curso {id_curso} (periodo {id_periodo}).")
        return
    CUR.execute("""
        INSERT INTO matricula (id_estudiante, id_curso, id_aula, id_periodo)
        VALUES (%s, %s, %s, %s)
    """, (id_estudiante, id_curso, id_aula, id_periodo))
    CONN.commit()
    print(f"✅ Matrícula creada (estudiante {id_estudiante} → curso {id_curso}, aula {id_aula}, periodo {id_periodo}).")

def resumen_matriculas():
    CUR.execute("""
        SELECT e.codigo, e.nombres AS estudiante, e.apellidos,
               c.nombre AS curso, c.codigo AS cod_curso,
               d.nombres AS docente, d.apellidos AS docente_apellidos,
               p.nombre AS periodo,
               a.nombre AS aula, a.ubicacion
        FROM matricula m
        JOIN estudiante e ON m.id_estudiante = e.id_estudiante
        JOIN curso c ON m.id_curso = c.id_curso
        LEFT JOIN docente d ON c.id_docente = d.id_docente
        JOIN periodo p ON m.id_periodo = p.id_periodo
        JOIN aula a ON m.id_aula = a.id_aula
        ORDER BY e.codigo, c.id_curso;
    """)
    rows = CUR.fetchall()
    print("\n📋 Resumen de matrículas:")
    if rows:
        print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No hay matrículas registradas aún.")

def main():
    print("===== REGISTRO DE ESTUDIANTE + MATRÍCULA (BD: dbia) =====")
    id_periodo = seleccionar_periodo()

    while True:
        print("\n--- Datos del estudiante ---")
        codigo = input("Código institucional: ").strip()
        nombres = input("Nombres: ").strip()
        apellidos = input("Apellidos: ").strip()
        dni = input("DNI (8 dígitos): ").strip()

        id_est = upsert_estudiante(codigo, nombres, apellidos, dni)

        # cursos y aulas
        cursos_ids = listar_cursos()
        aulas_ids = listar_aulas()

        ids_cursos_elegidos = input("\nIngrese ID(s) de curso a matricular (separados por coma): ").strip()
        try:
            cursos_elegidos = [int(x) for x in ids_cursos_elegidos.split(",") if x.strip()]
        except ValueError:
            print("Entrada inválida de cursos.")
            continue

        id_aula = None
        while id_aula is None:
            try:
                ida = int(input("Ingrese ID de aula: ").strip())
                if ida in aulas_ids:
                    id_aula = ida
                else:
                    print("ID de aula no válido.")
            except ValueError:
                print("Ingrese un número válido.")

        for c_id in cursos_elegidos:
            if c_id not in cursos_ids:
                print(f"ID de curso inválido: {c_id}. Saltando…")
                continue
            matricular(id_est, c_id, id_aula, id_periodo)

        otra = input("\n¿Registrar otro estudiante? (s/n): ").lower().strip()
        if otra != 's':
            break

    resumen_matriculas()

if __name__ == "__main__":
    try:
        main()
    finally:
        CUR.close()
        CONN.close()
