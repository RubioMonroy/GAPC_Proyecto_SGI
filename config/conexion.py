# config/conexion.py
import mysql.connector
import streamlit as st

def obtener_conexion():
    """
    Usa st.secrets para leer credenciales:
      st.secrets["db_host"], st.secrets["db_user"], st.secrets["db_password"], st.secrets["db_name"], (opcional) db_port
    Devuelve una conexión mysql.connector o None si falla.
    """
    try:
        host = st.secrets["db_host"]
        user = st.secrets["db_user"]
        password = st.secrets["db_password"]
        database = st.secrets["db_name"]
        port = int(st.secrets.get("db_port", 3306))
    except Exception as e:
        st.error("⚠️ Faltan credenciales en st.secrets. Revisa .streamlit/secrets.toml o Streamlit Cloud secrets.")
        return None

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=False
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"⚠️ Error conectando a la base de datos: {e}")
        return None
