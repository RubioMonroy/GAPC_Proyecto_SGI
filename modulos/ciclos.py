# modulos/ciclos.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_ciclos():
    require_login()
    st.title("Ciclos")
    conn = obtener_conexion()
    if not conn:
        st.error("No hay conexión.")
        return
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM ciclos ORDER BY id_ciclo DESC")
    st.table(cur.fetchall())

    st.subheader("Crear ciclo")
    fecha_inicio = st.date_input("Fecha inicio")
    if st.button("Crear ciclo"):
        try:
            cur.execute("INSERT INTO ciclos (id_gapc, fecha_inicio) VALUES (%s, %s)", (1, fecha_inicio))
            conn.commit()
            st.success("Ciclo creado.")
            st.experimental_rerun()
        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

    cur.close()
    conn.close()
