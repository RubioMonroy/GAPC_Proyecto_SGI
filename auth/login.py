# auth/login.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import iniciar_sesion
from datetime import datetime

def verificar_usuario(usuario, contraseña):
    con = obtener_conexion()
    if not con:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE usuario = %s AND estado = 'activo'"
        cursor.execute(query, (usuario,))
        row = cursor.fetchone()
        if not row:
            return None

        # Comparación sencilla: texto plano o posterior compatibilidad con hash
        if contraseña == row["contraseña"]:
            # actualizar ultimo_login y resetear intentos
            try:
                cursor.execute("UPDATE usuarios SET ultimo_login = %s, intentos_fallidos = 0 WHERE id_usuario = %s", (datetime.now(), row["id_usuario"]))
                con.commit()
            except:
                con.rollback()
            return row

        # contraseña incorrecta: incrementar contador
        try:
            cursor.execute("UPDATE usuarios SET intentos_fallidos = intentos_fallidos + 1 WHERE id_usuario = %s", (row["id_usuario"],))
            con.commit()
        except:
            con.rollback()
        return None

    finally:
        con.close()


def login():
    st.title("Inicio de sesión")
    with st.form("login_form", clear_on_submit=False):
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar sesión")
        if submitted:
            datos = verificar_usuario(usuario, contraseña)
            if datos:
                iniciar_sesion(datos)
                st.success(f"Bienvenido/a {datos.get('usuario')}")
                st.experimental_rerun()
            else:
                st.error("Credenciales incorrectas o usuario inactivo.")
