import streamlit as st
from modulos.config.conexion import obtener_conexion

def verificar_usuario(usuario, contraseña):
    con = obtener_conexion()

    if not con:
        st.error("⚠️ No se pudo conectar a la base de datos.")
        return None

    try:
        cursor = con.cursor()

        query = """
            SELECT usuario 
            FROM usuarios
            WHERE usuario = %s AND contraseña = %s AND activo = 1
        """

        cursor.execute(query, (usuario, contraseña))
        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        con.close()


def login():
    st.title("Inicio de sesión")

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        datos = verificar_usuario(usuario, contraseña)

        if datos:
            st.session_state["usuario"] = datos
            st.session_state["sesion_iniciada"] = True
            st.success(f"Bienvenido 👋 {datos}")
            st.rerun()
        else:
            st.error("❌ Credenciales incorrectas o usuario inactivo.")

