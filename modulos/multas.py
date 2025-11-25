# modulos/multas.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_multas():
    require_login()
    st.title("Multas")
    conn = obtener_conexion()
    if not conn:
        st.error("Sin conexión")
        return
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT m.*, s.nombres, s.apellidos FROM multas m LEFT JOIN socios s ON m.id_socio = s.id_socio ORDER BY m.fecha_generada DESC")
    st.table(cur.fetchall() or [])
    cur.close()
    conn.close()
