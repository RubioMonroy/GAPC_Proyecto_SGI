# modulos/reuniones.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_reuniones():
    require_login()
    st.title("Reuniones")
    conn = obtener_conexion()
    if not conn:
        st.error("No hay conexión.")
        return
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT r.*, c.fecha_inicio FROM reuniones r LEFT JOIN ciclos c ON r.id_ciclo = c.id_ciclo ORDER BY r.fecha DESC")
    st.table(cur.fetchall())

    st.subheader("Crear reunión")
    fecha = st.date_input("Fecha")
    descripcion = st.text_input("Descripción")
    if st.button("Crear reunión"):
        try:
            cur.execute("INSERT INTO reuniones (id_ciclo, fecha, descripcion) VALUES (%s, %s, %s)", (1, fecha, descripcion))
            conn.commit()
            st.success("Reunión creada.")
            st.experimental_rerun()
        except Exception as e:
            conn.rollback()
            st.error(str(e))

    cur.close()
    conn.close()
