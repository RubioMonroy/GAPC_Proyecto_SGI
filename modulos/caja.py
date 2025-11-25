# modulos/caja.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_caja():
    require_login()
    st.title("Caja")
    conn = obtener_conexion()
    if not conn:
        st.error("Sin conexión")
        return
    cur = conn.cursor(dictionary=True)

    st.subheader("Registrar caja (prueba)")
    saldo_apertura = st.number_input("saldo_apertura", format="%.2f")
    multas_pagadas = st.number_input("multas_pagadas", format="%.2f")
    ahorros = st.number_input("ahorros", format="%.2f")
    otras_actividades = st.number_input("otras_actividades", format="%.2f")
    total_pago_prestamos = st.number_input("pago préstamos (capital+interés)", format="%.2f")
    retiro_ahorros = st.number_input("retiro_ahorros", format="%.2f")
    total_desembolso_prestamos = st.number_input("desembolso_prestamos", format="%.2f")

    if st.button("Guardar caja"):
        try:
            saldo_cierre = saldo_apertura + multas_pagadas + ahorros + otras_actividades + total_pago_prestamos - (retiro_ahorros + total_desembolso_prestamos)
            cur.execute("""
                INSERT INTO caja (id_reunion, saldo_apertura, multas_pagadas, ahorros, otras_actividades, otros_ingresos_grupo,
                                  total_pago_prestamos, retiro_ahorros, otros_gastos_grupo, total_desembolso_prestamos, saldo_cierre)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (1, saldo_apertura, multas_pagadas, ahorros, otras_actividades, 0.00, total_pago_prestamos, retiro_ahorros, 0.00, total_desembolso_prestamos, saldo_cierre))
            conn.commit()
            st.success("Registro de caja guardado.")
            st.experimental_rerun()
        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

    # mostrar últimos registros
    cur.execute("SELECT * FROM caja ORDER BY id_caja DESC LIMIT 10")
    st.table(cur.fetchall() or [])

    cur.close()
    conn.close()
