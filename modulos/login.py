import streamlit as st
from modulos.config.conexion import obtener_conexion


def verificar_usuario(usuario, contraseña):
    con = obtener_conexion()
    if not con:
        st.error("⚠️ No se pudo conectar a la base de datos.")
        return None

    # Guardar estado
    st.session_state["conexion_exitosa"] = True

    try:
        cursor = con.cursor()

        # Consulta EXACTA según tu tabla
        query = """
            SELECT usuario 
            FROM usuarios
            WHERE usuario = %s AND contraseña = %s
        """

        cursor.execute(query, (usuario, contraseña))
        result = cursor.fetchone()

        # Si coincide, retorna el usuario
        return result[0] if result else None

    finally:
        con.close()


def login():
    st.title("Inicio de sesión")

    if st.session_state.get("conexion_exitosa"):
        st.success("✅ Conexión con la base de datos establecida.")

    usuario = st.text_input("Usuario", key="usuario_input")
    contraseña = st.text_input("Contraseña", type="password", key="contraseña_input")

    if st.button("Iniciar sesión"):
        resultado = verificar_usuario(usuario, contraseña)

        if resultado:
            st.session_state["usuario"] = resultado
            st.session_state["sesion_iniciada"] = True
            st.success(f"Bienvenido 👋 {resultado}")
            st.rerun()
        else:
            st.error("❌ Credenciales incorrectas.")

