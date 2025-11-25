# modulos/ahorros.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_ahorros():
    require_login()
    st.title("Ahorros / aportes")
    conn = obtener_conexion()
    if not conn:
        st.error("Sin conexión")
        return
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM socios")
    socios = cur.fetchall() or []

    for s in socios:
        monto = st.number_input(f"Ahorro - {s['nombres']} {s['apellidos']}", min_value=0.0, format="%.2f", key=f"ah_{s['id_socio']}")
        if st.button(f"Guardar ahorro {s['id_socio']}", key=f"gah_{s['id_socio']}"):
            try:
                cur.execute("INSERT INTO ahorros (id_socio, id_reunion, ahorro, fecha) VALUES (%s,%s,%s,CURDATE())", (s['id_socio'], 1, monto))
                cur.execute("INSERT INTO aportes (id_socio, id_reunion, monto, tipo, fecha) VALUES (%s,%s,%s,%s,CURDATE())", (s['id_socio'],1,monto,'ahorro'))
                conn.commit()
                st.success("Ahorro registrado.")
            except Exception as e:
                conn.rollback()
                st.error(f"Error: {e}")

    cur.close()
    conn.close()
