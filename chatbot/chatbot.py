from datetime import date

from chatbot.state_machine import EstadoConversacion

from services.vacation_service import (
    buscar_empleado_por_legajo,
    convertir_fecha,
    calcular_dias_solicitados,
    tiene_saldo_suficiente,
    crear_solicitud_vacaciones,
    calcular_saldo_restante
)


class ChatbotVacaciones:

    def __init__(self, session_state):

        self.session_state = session_state

        if "estado_conversacion" not in self.session_state:
            self.session_state.estado_conversacion = (
                EstadoConversacion.BIENVENIDA
            )

        if "contexto" not in self.session_state:
            self.session_state.contexto = {}

    def iniciar_conversacion(self):

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_LEGAJO
        )

        return (
            "Hola, soy el asistente de gestión de vacaciones.\n\n"
            "Por favor ingresá tu número de legajo."
        )

    def procesar_mensaje(self, mensaje_usuario):

        estado = self.session_state.estado_conversacion

        if estado == EstadoConversacion.BIENVENIDA:
            return self.iniciar_conversacion()

        if estado == EstadoConversacion.ESPERANDO_LEGAJO:
            return self._procesar_legajo(mensaje_usuario)

        if estado == EstadoConversacion.ESPERANDO_FECHA_INICIO:
            return self._procesar_fecha_inicio(mensaje_usuario)

        if estado == EstadoConversacion.ESPERANDO_FECHA_FIN:
            return self._procesar_fecha_fin(mensaje_usuario)

        if estado == EstadoConversacion.FINALIZADO:
            return (
                "La solicitud ya finalizó.\n\n"
                "Presioná Reiniciar para comenzar nuevamente."
            )

        return "Estado no reconocido."

    def _procesar_legajo(self, mensaje_usuario):

        legajo = mensaje_usuario.strip()

        if not legajo.isdigit():
            return (
                "El legajo debe contener únicamente números.\n\n"
                "Por favor ingresá un legajo válido."
            )

        empleado = buscar_empleado_por_legajo(
            legajo
        )

        if empleado is None:
            return (
                "No existe un empleado con ese legajo.\n\n"
                "Ingresá nuevamente el número de legajo."
            )

        self.session_state.contexto["empleado"] = empleado

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_FECHA_INICIO
        )

        return (
            f"Empleado encontrado: {empleado['nombre']}.\n\n"
            f"Días disponibles: {empleado['dias_disponibles']}.\n\n"
            "Ingresá la fecha de inicio (DD/MM/AAAA)."
        )

    def _procesar_fecha_inicio(self, mensaje_usuario):

        fecha_inicio = convertir_fecha(
            mensaje_usuario.strip()
        )

        if fecha_inicio is None:
            return (
                "La fecha ingresada no es válida.\n\n"
                "Utilizá el formato DD/MM/AAAA."
            )

        fecha_actual = date.today()

        if fecha_inicio < fecha_actual:
            return (
                "La fecha de inicio no puede ser anterior a la fecha actual.\n\n"
                "Ingresá una fecha válida."
            )

        self.session_state.contexto[
            "fecha_inicio"
        ] = fecha_inicio

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_FECHA_FIN
        )

        return (
            "Ingresá la fecha de finalización "
            "(DD/MM/AAAA)."
        )

    def _procesar_fecha_fin(self, mensaje_usuario):

        fecha_fin = convertir_fecha(
            mensaje_usuario.strip()
        )

        if fecha_fin is None:
            return (
                "La fecha ingresada no es válida.\n\n"
                "Utilizá el formato DD/MM/AAAA."
            )

        fecha_inicio = (
            self.session_state.contexto["fecha_inicio"]
        )

        if fecha_fin < fecha_inicio:
            return (
                "La fecha de finalización no puede ser "
                "anterior a la fecha de inicio."
            )

        empleado = (
            self.session_state.contexto["empleado"]
        )

        dias_solicitados = calcular_dias_solicitados(
            fecha_inicio,
            fecha_fin
        )

        saldo_restante = calcular_saldo_restante(
            empleado,
            dias_solicitados
        )

        self.session_state.contexto["saldo_restante"] = saldo_restante

        if not tiene_saldo_suficiente(
            empleado,
            dias_solicitados
        ):

            crear_solicitud_vacaciones(
                empleado,
                fecha_inicio,
                fecha_fin,
                dias_solicitados,
                "RECHAZADA_SIN_SALDO"
            )

            self.session_state.contexto = {}

            self.session_state.estado_conversacion = (
                EstadoConversacion.ESPERANDO_LEGAJO
            )

            return (
                f"Solicitud rechazada.\n\n"
                f"Días solicitados: {dias_solicitados}\n"
                f"Días disponibles: {empleado['dias_disponibles']}\n\n"
                f"Saldo restante: {saldo_restante}\n\n"
                "Para iniciar una nueva solicitud, ingresá otro número de legajo."
            )

        if dias_solicitados > 5:

            crear_solicitud_vacaciones(
                empleado,
                fecha_inicio,
                fecha_fin,
                dias_solicitados,
                "PENDIENTE_SUPERVISOR"
            )

            self.session_state.estado_conversacion = (
                EstadoConversacion.ESPERANDO_APROBACION_SUPERVISOR
            )

            return (
                f"La solicitud fue registrada.\n\n"
                f"Días solicitados: {dias_solicitados}\n\n"
                f"Supervisor asignado: "
                f"{empleado['supervisor']}\n\n"
                f"Estado: Pendiente de aprobación."
            )

        crear_solicitud_vacaciones(
            empleado,
            fecha_inicio,
            fecha_fin,
            dias_solicitados,
            "PREAPROBADA"
        )

        self.session_state.contexto = {}

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_LEGAJO
        )

        return (
            f"Solicitud preaprobada automáticamente.\n\n"
            f"Días solicitados: {dias_solicitados}\n\n"
            f"Saldo restante: {saldo_restante}\n\n"
            "Para iniciar una nueva solicitud, ingresá otro número de legajo."
        )

    def aprobar_solicitud(self):

        self.session_state.contexto = {}

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_LEGAJO
        )
        return (
            "El supervisor aprobó la solicitud.\n\n"
            "Para iniciar una nueva solicitud, ingresá otro número de legajo."
        )

    def rechazar_solicitud(self):

        self.session_state.contexto = {}

        self.session_state.estado_conversacion = (
            EstadoConversacion.ESPERANDO_LEGAJO
        )

        return (
            "El supervisor rechazó la solicitud.\n\n"
            "Para iniciar una nueva solicitud, ingresá otro número de legajo."
        )