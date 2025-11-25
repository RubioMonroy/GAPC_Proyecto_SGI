# modulos/asistencia.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

MULTA = 5.00

def vista_asistencia():
    require_login()
    st.title("Registro de asistencia")

    conn = obtener_conexion()
    if not conn:
        st.error("Sin conexión.")
        return
    cur = conn.cursor(dictionary=True)

    # Obtener última reunión
    cur.execute("SELECT * FROM reuniones ORDER BY fecha DESC LIMIT 1")
    reunion = cur.fetchone()
    if not reunion:
        st.info("No hay reuniones. Crea una en Reuniones.")
        return

    st.write(f"Reunión: {reunion['id_reunion']} - {reunion['fecha']}")

    cur.execute("SELECT * FROM socios")
    socios = cur.fetchall() or []

    for s in socios:
        key = f"chk_{s['id_socio']}"
        checked = st.checkbox(f"{s['nombres']} {s['apellidos']}", value=True, key=key)
        if st.button(f"Guardar {s['id_socio']}", key=f"g_{s['id_socio']}"):
            estado = "asistio" if checked else "falto"
            multa = 0.00 if checked else MULTA
            try:
                cur.execute("INSERT INTO asistencias (id_reunion, id_socio, estado, multa_generada, fecha) VALUES (%s,%s,%s,%s,CURDATE())",
                            (reunion['id_reunion'], s['id_socio'], estado, multa))
                if multa > 0:
                    cur.execute("INSERT INTO multas (id_socio, id_reunion, monto, motivo, fecha_generada) VALUES (%s,%s,%s,%s,CURDATE())",
                                (s['id_socio'], reunion['id_reunion'], multa, 'inasistencia'))
                conn.commit()
                st.success("Registro guardado.")
            except Exception as e:
                conn.rollback()
                st.error(f"Error: {e}")

    cur.close()
    conn.close()
