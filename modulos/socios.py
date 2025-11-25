# modulos/socios.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_socios():
    require_login()
    st.title("Gestión de socios")
    conn = obtener_conexion()
    if not conn:
        st.error("No hay conexión a DB.")
        return
    cur = conn.cursor(dictionary=True)

    st.subheader("Lista de socios")
    cur.execute("SELECT * FROM socios")
    rows = cur.fetchall() or []
    st.table(rows)

    st.subheader("Agregar socio")
    nombres = st.text_input("Nombres")
    apellidos = st.text_input("Apellidos")
    telefono = st.text_input("Teléfono")
    direccion = st.text_area("Dirección")

    if st.button("Guardar socio"):
        try:
            cur.execute("INSERT INTO socios (id_gapc, nombres, apellidos, telefono, direccion, fecha_ingreso) VALUES (%s,%s,%s,%s,%s,CURDATE())",
                        (1, nombres, apellidos, telefono, direccion))
            conn.commit()
            st.success("Socio agregado.")
            st.experimental_rerun()
        except Exception as e:
            conn.rollback()
            st.error(f"Error al guardar: {e}")

    cur.close()
    conn.close()
