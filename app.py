# app.py
import streamlit as st
from modulos.asistencia import mostrar_asistencia  # Importamos la función mostrar_asistencia del módulo asistencia
from modulos.login import login

# Llamamos a la función mostrar_asistencia para mostrar el mensaje en la app
mostrar_asistencia()
login()
