import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_EMPLEADOS = BASE_DIR / "data" / "empleados.csv"
ARCHIVO_SOLICITUDES = BASE_DIR / "data" / "solicitudes_vacaciones.csv"


CAMPOS_SOLICITUD = [
    "id",
    "legajo",
    "empleado",
    "sector",
    "supervisor",
    "fecha_inicio",
    "fecha_fin",
    "dias_solicitados",
    "estado"
]


def cargar_empleados():
    empleados = []

    with open(
        ARCHIVO_EMPLEADOS,
        "r",
        encoding="utf-8",
        newline=""
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["dias_disponibles"] = int(
                fila["dias_disponibles"]
            )
            empleados.append(fila)

    return empleados


def cargar_solicitudes():
    solicitudes = []

    with open(
        ARCHIVO_SOLICITUDES,
        "r",
        encoding="utf-8",
        newline=""
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            solicitudes.append(fila)

    return solicitudes


def guardar_solicitudes(solicitudes):
    with open(
        ARCHIVO_SOLICITUDES,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=CAMPOS_SOLICITUD
        )

        escritor.writeheader()
        escritor.writerows(solicitudes)


def buscar_empleado_por_legajo(legajo):
    empleados = cargar_empleados()

    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado

    return None


def convertir_fecha(texto_fecha):
    try:
        return datetime.strptime(
            texto_fecha,
            "%d/%m/%Y"
        ).date()
    except ValueError:
        return None


def calcular_dias_solicitados(
    fecha_inicio,
    fecha_fin
):
    return (fecha_fin - fecha_inicio).days + 1


def tiene_saldo_suficiente(
    empleado,
    dias_solicitados
):
    return (
        empleado["dias_disponibles"]
        >= dias_solicitados
    )


def crear_solicitud_vacaciones(
    empleado,
    fecha_inicio,
    fecha_fin,
    dias_solicitados,
    estado
):
    solicitudes = cargar_solicitudes()

    nueva_solicitud = {
        "id": str(uuid4()),
        "legajo": empleado["legajo"],
        "empleado": empleado["nombre"],
        "sector": empleado["sector"],
        "supervisor": empleado["supervisor"],
        "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
        "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
        "dias_solicitados": str(dias_solicitados),
        "estado": estado
    }

    solicitudes.append(nueva_solicitud)

    guardar_solicitudes(solicitudes)

    return nueva_solicitud