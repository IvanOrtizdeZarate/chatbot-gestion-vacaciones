import streamlit as st

from chatbot.chatbot import ChatbotVacaciones
from chatbot.state_machine import EstadoConversacion


st.set_page_config(
    page_title="Gestión de Vacaciones",
    page_icon="🏖️"
)

st.title("Chatbot de Gestión de Vacaciones")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

chatbot = ChatbotVacaciones(
    st.session_state
)

if st.button("Reiniciar conversación"):
    st.session_state.clear()
    st.rerun()

if len(st.session_state.mensajes) == 0:

    respuesta_inicial = (
        chatbot.iniciar_conversacion()
    )

    st.session_state.mensajes.append({
        "rol": "assistant",
        "contenido": respuesta_inicial
    })

for mensaje in st.session_state.mensajes:

    with st.chat_message(
        mensaje["rol"]
    ):
        st.markdown(
            mensaje["contenido"]
        )

if (
    st.session_state.estado_conversacion
    == EstadoConversacion.ESPERANDO_APROBACION_SUPERVISOR
):

    st.divider()

    st.subheader(
        "Simulación de Supervisor"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Aprobar Solicitud"
        ):

            respuesta = (
                chatbot.aprobar_solicitud()
            )

            st.session_state.mensajes.append({
                "rol": "assistant",
                "contenido": respuesta
            })

            st.rerun()

    with col2:

        if st.button(
            "Rechazar Solicitud"
        ):

            respuesta = (
                chatbot.rechazar_solicitud()
            )

            st.session_state.mensajes.append({
                "rol": "assistant",
                "contenido": respuesta
            })

            st.rerun()

mensaje_usuario = st.chat_input(
    "Escribí tu respuesta..."
)

if mensaje_usuario:

    st.session_state.mensajes.append({
        "rol": "user",
        "contenido": mensaje_usuario
    })

    respuesta = chatbot.procesar_mensaje(
        mensaje_usuario
    )

    st.session_state.mensajes.append({
        "rol": "assistant",
        "contenido": respuesta
    })

    st.rerun()