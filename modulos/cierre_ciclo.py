# modulos/cierre_ciclo.py
import streamlit as st
from config.conexion import obtener_conexion
from auth.session import require_login

def vista_cierre():
    require_login()
    st.title("Cierre de ciclo (prueba)")
    conn = obtener_conexion()
    if not conn:
        st.error("Sin conexión")
        return
    cur = conn.cursor(dictionary=True)

    if st.button("Ejecutar cierre piloto"):
        try:
            # cálculos simplificados: totales de ahorros, multas, desembolsos, retiros
            cur.execute("SELECT COALESCE(SUM(ahorro),0) as total_ahorros FROM ahorros")
            total_ahorros = cur.fetchone().get("total_ahorros") or 0.0

            cur.execute("SELECT COALESCE(SUM(monto),0) as total_multas FROM multas")
            total_multas = cur.fetchone().get("total_multas") or 0.0

            cur.execute("SELECT COALESCE(SUM(total_desembolso_prestamos),0) as desembolsos FROM caja")
            desembolsos = cur.fetchone().get("desembolsos") or 0.0

            # para la prueba, forzamos que sobrante sea 0
            sobrante = 0.00

            cur.execute("INSERT INTO cierre_ciclo (id_ciclo, fecha, total_ahorro_grupo, total_fondo_grupo, sobrante) VALUES (%s,CURDATE(),%s,%s,%s)",
                        (1, total_ahorros, total_multas, sobrante))
            conn.commit()
            st.success("Cierre de ciclo registrado (piloto). Sobrante forzado a 0.")
            st.experimental_rerun()
        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

    # mostrar últimos cierres
    cur.execute("SELECT * FROM cierre_ciclo ORDER BY id_cierre DESC LIMIT 10")
    st.table(cur.fetchall() or [])

    cur.close()
    conn.close()
