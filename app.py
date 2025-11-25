# app.py
import streamlit as st
from auth.login import login
from auth.session import usuario_actual, cerrar_sesion
from modulos.socios import vista_socios
from modulos.ciclos import vista_ciclos
from modulos.reuniones import vista_reuniones
from modulos.asistencia import vista_asistencia
from modulos.ahorros import vista_ahorros
from modulos.multas import vista_multas
from modulos.caja import vista_caja
from modulos.cierre_ciclo import vista_cierre

st.set_page_config(page_title="GAPC - SGI", layout="wide")

if "sesion_iniciada" not in st.session_state:
    st.session_state["sesion_iniciada"] = False

if not st.session_state["sesion_iniciada"]:
    login()
else:
    st.sidebar.title("Menú GAPC - SGI")
    opcion = st.sidebar.selectbox(
        "Sección",
        ["Panel","Socios","Ciclos","Reuniones","Asistencia","Ahorros","Multas","Caja","Cierre de Ciclo","Cerrar sesión"]
    )

    if opcion == "Panel":
        st.header("Panel principal")
        st.write(f"Usuario: **{st.session_state.get('usuario')}** | Rol: **{st.session_state.get('rol')}**")
    elif opcion == "Socios":
        vista_socios()
    elif opcion == "Ciclos":
        vista_ciclos()
    elif opcion == "Reuniones":
        vista_reuniones()
    elif opcion == "Asistencia":
        vista_asistencia()
    elif opcion == "Ahorros":
        vista_ahorros()
    elif opcion == "Multas":
        vista_multas()
    elif opcion == "Caja":
        vista_caja()
    elif opcion == "Cierre de Ciclo":
        vista_cierre()
    elif opcion == "Cerrar sesión":
        cerrar_sesion()
        st.experimental_rerun()
