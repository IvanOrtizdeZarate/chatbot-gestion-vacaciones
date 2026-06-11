# Chatbot de Gestión de Vacaciones

## Descripción

Proyecto desarrollado para la materia Organización Empresarial.

El objetivo del sistema es automatizar el proceso de solicitud de vacaciones mediante un chatbot web, reemplazando tareas manuales realizadas por Recursos Humanos y reduciendo tiempos de gestión.

El chatbot guía al empleado durante la solicitud, valida las reglas de negocio y determina si la solicitud puede ser preaprobada automáticamente o si requiere la intervención de un supervisor.

---

## Tecnologías Utilizadas

* Python 3
* Streamlit
* CSV (persistencia de datos)
* Git y GitHub

---

## Estructura del Proyecto

```text
chatbot-gestion-vacaciones/
│
├── app.py
├── requirements.txt
├── README.md
│
├── chatbot/
│   ├── chatbot.py
│   └── state_machine.py
│
├── services/
│   └── vacation_service.py
│
├── data/
│   ├── empleados.csv
│   └── solicitudes_vacaciones.csv
│
└── docs/
    └── bpmn/
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

### 2. Ingresar al proyecto

```bash
cd chatbot-gestion-vacaciones
```

### 3. Instalar dependencias

```bash
py -m pip install -r requirements.txt
```

---

## Ejecución

```bash
py -m streamlit run app.py
```

Una vez iniciado, abrir la URL indicada por Streamlit en el navegador.

---

## Reglas de Negocio

* El legajo ingresado debe existir en el sistema.
* El legajo debe contener únicamente caracteres numéricos.
* La fecha de inicio no puede ser anterior a la fecha actual.
* La fecha de finalización no puede ser anterior a la fecha de inicio.
* El empleado debe poseer saldo suficiente de días de vacaciones.
* Las solicitudes de hasta 5 días son preaprobadas automáticamente.
* Las solicitudes de más de 5 días requieren aprobación del supervisor.
* Una vez aprobada la solicitud, el saldo de vacaciones disponible se actualiza automáticamente.

---

## Persistencia de Datos

El sistema utiliza archivos CSV para almacenar la información.

### empleados.csv

Contiene:

* Legajo
* Nombre
* Sector
* Supervisor
* Días disponibles

### solicitudes_vacaciones.csv

Contiene:

* ID de solicitud
* Legajo
* Empleado
* Sector
* Supervisor
* Fecha de inicio
* Fecha de finalización
* Días solicitados
* Estado de la solicitud

---

## Diagramas BPMN

Los diagramas utilizados para modelar el proceso se encuentran en:

```text
docs/bpmn/
```

* Proceso AS-IS
* Proceso TO-BE

---

## Autores

Trabajo Práctico Integrador – Organización Empresarial

Desarrollado por:

* Iván Ortiz
