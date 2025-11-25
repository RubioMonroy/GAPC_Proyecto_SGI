# GAPC_Proyecto_SGI - Streamlit app (piloto)

## Requisitos
- Python 3.9+
- Streamlit
- mysql-connector-python

## Instalación
1. Crear la BD y tablas necesarias en phpMyAdmin (importar SQL del proyecto).
2. Ejecutar `sql/usuarios_fix.sql` para crear usuarios piloto (admin / admin123).
3. Crear en Streamlit Cloud `.streamlit/secrets.toml` con:
   db_host = "localhost"
   db_user = "root"
   db_password = ""
   db_name = "gapc"
   db_port = "3306"
4. Instalar dependencias:
   pip install -r requirements.txt
5. Ejecutar:
   streamlit run app.py

## Usuarios de prueba
- admin / admin123
- usuariopiloto / abcd1234

## Nota
Contraseñas actualmente en texto plano para pruebas. Agregar hashing en producción.
Documento de referencia: `/mnt/data/Proyecto-final_merged.pdf`
