import streamlit as st
import requests

# 1. Configuración de credenciales de JSONBin
BIN_ID = "6a7566a3da38895dfec48c54"  
API_KEY = "$2a$10$fhgij9c5sO3ezqwOcJi0u.V7MHzvSaLRPqlOfpkziPwfZByxDc9SG" 
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# 2. Función para actualizar la nube
def actualizar_estado_nube(nuevos_estados):
    try:
        respuesta = requests.put(URL, json=nuevos_estados, headers=HEADERS)
        if respuesta.status_code == 200:
            st.success("✅ Nube actualizada con éxito", icon="☁️")
        else:
            st.error(f"Error al actualizar la nube: {respuesta.status_code}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# 3. Interfaz del Panel de Control
st.title("🎛️ Panel de Control - Evento Indpulsa")
st.write("Los cambios realizados aquí se reflejarán automáticamente en la web.")
st.markdown("---")

# 4. Estado inicial de TODAS las actividades con los IDs exactos del HTML
if 'estados' not in st.session_state:
    st.session_state.estados = {
        "lunes-t1": "PENDIENTE", "lunes-t2": "PENDIENTE", "lunes-t3": "PENDIENTE", "lunes-t4": "PENDIENTE", "lunes-t5": "PENDIENTE", "lunes-t6": "PENDIENTE",
        "martes-t1": "PENDIENTE", "martes-t2": "PENDIENTE", "martes-t3": "PENDIENTE", "martes-t4": "PENDIENTE", "martes-t5": "PENDIENTE", "martes-t6": "PENDIENTE",
        "miercoles-t1": "PENDIENTE", "miercoles-t2": "PENDIENTE", "miercoles-t3": "PENDIENTE", "miercoles-t4": "PENDIENTE", "miercoles-t5": "PENDIENTE", "miercoles-t6": "PENDIENTE", "miercoles-t7": "PENDIENTE", "miercoles-t8": "PENDIENTE",
        "jueves-t1": "PENDIENTE", "jueves-t2": "PENDIENTE", "jueves-t3": "PENDIENTE", "jueves-t4": "PENDIENTE", "jueves-t5": "PENDIENTE", "jueves-t6": "PENDIENTE", "jueves-t7": "PENDIENTE", "jueves-t8": "PENDIENTE",
        "viernes-t1": "PENDIENTE", "viernes-t2": "PENDIENTE", "viernes-t3": "PENDIENTE"
    }

# 5. Estructura de las actividades con sus nombres reales para la interfaz
talleres_por_dia = {
    "Lunes": [
        ("lunes-t1", "Lanzamiento de Indpulsa"),
        ("lunes-t2", "Presentación del Problema"),
        ("lunes-t3", "Coffee Break"),
        ("lunes-t4", "Conversatorio"),
        ("lunes-t5", "Charla CODELCO"),
        ("lunes-t6", "Actividad de Acercamiento")
    ],
    "Martes": [
        ("martes-t1", "Visita a Empresas"),
        ("martes-t2", "Coffee Break"),
        ("martes-t3", "Industria 4.0 aplicada"),
        ("martes-t4", "Charla RRHH"),
        ("martes-t5", "Cómo Innovan las Empresas"),
        ("martes-t6", "Charla CORFO")
    ],
    "Miércoles": [
        ("miercoles-t1", "Charla Arauco"),
        ("miercoles-t2", "Cscueqqcecdlh"),
        ("miercoles-t3", "Taller IA"),
        ("miercoles-t4", "Del Pitch al Piloto"),
        ("miercoles-t5", "Compitiendo en Silicon Valley"),
        ("miercoles-t6", "El Nuevo Techo de Contratación"),
        ("miercoles-t7", "Kick Off Innovación"),
        ("miercoles-t8", "Speed Mentoring")
    ],
    "Jueves": [
        ("jueves-t1", "Charla Pares&Alvarez"),
        ("jueves-t2", "Charla Valmar"),
        ("jueves-t3", "Charla Anatomia de un Pitch Ganador"),
        ("jueves-t4", "Charla Financiamiento"),
        ("jueves-t5", "Coffee Break"),
        ("jueves-t6", "Mentoring With CEOS"),
        ("jueves-t7", "De la Universidad al Mundo"),
        ("jueves-t8", "Founders en tus 20's")
    ],
    "Viernes": [
        ("viernes-t1", "El desafio Industrial"),
        ("viernes-t2", "Coffee Break"),
        ("viernes-t3", "Cierre y Premiación")
    ]
}

# 6. Generación automática de la interfaz
for dia, talleres in talleres_por_dia.items():
    st.header(f"📅 {dia}")
    
    for key, nombre in talleres:
        st.subheader(f"🔹 {nombre}")
        st.info(f"Estado actual: **{st.session_state.estados[key]}**")
        
        col1, col2, col3 = st.columns(3)
        
        # Botones dinámicos para cada actividad
        if col1.button("🕒 Pendiente", key=f"btn_p_{key}"):
            st.session_state.estados[key] = "PENDIENTE"
            actualizar_estado_nube(st.session_state.estados)
            st.rerun()

        if col2.button("▶️ En Proceso", key=f"btn_e_{key}"):
            st.session_state.estados[key] = "EN PROCESO"
            actualizar_estado_nube(st.session_state.estados)
            st.rerun()

        if col3.button("✅ Finalizado", key=f"btn_f_{key}"):
            st.session_state.estados[key] = "FINALIZADO"
            actualizar_estado_nube(st.session_state.estados)
            st.rerun()
            
    st.markdown("---") # Línea divisoria al final de cada día