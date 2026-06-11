import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_EMPLEADOS = BASE_DIR / "data" / "employees.json"
ARCHIVO_SOLICITUDES = BASE_DIR / "data" / "vacation_requests.json"


def cargar_empleados():
    with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_solicitudes():
    with open(ARCHIVO_SOLICITUDES, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_solicitudes(solicitudes):
    with open(ARCHIVO_SOLICITUDES, "w", encoding="utf-8") as archivo:
        json.dump(
            solicitudes,
            archivo,
            indent=2,
            ensure_ascii=False
        )


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
        "dias_solicitados": dias_solicitados,
        "estado": estado
    }

    solicitudes.append(nueva_solicitud)

    guardar_solicitudes(solicitudes)

    return nueva_solicitud