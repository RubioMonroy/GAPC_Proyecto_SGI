import streamlit as st
import mysql.connector

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
        )
    except Exception as e:
        st.error("❌ Error al conectar a la base de datos.")
        st.error(str(e))
        return None

