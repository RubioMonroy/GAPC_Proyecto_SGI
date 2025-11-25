# auth/session.py
import streamlit as st

def iniciar_sesion(datos_usuario):
    st.session_state["sesion_iniciada"] = True
    st.session_state["usuario"] = datos_usuario.get("usuario")
    st.session_state["rol"] = datos_usuario.get("rol", "facilitador")
    st.session_state["id_usuario"] = datos_usuario.get("id_usuario")

def cerrar_sesion():
    for k in ["sesion_iniciada", "usuario", "rol", "id_usuario", "conexion_exitosa"]:
        if k in st.session_state:
            del st.session_state[k]

def usuario_actual():
    return st.session_state.get("usuario")

def require_login():
    if not st.session_state.get("sesion_iniciada"):
        st.warning("Debe iniciar sesión para acceder.")
        st.stop()
