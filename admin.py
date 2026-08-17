import streamlit as st
import requests

# 1. Configuración de credenciales de JSONBin
BIN_ID = "6a7566a3da38895dfec48c54"  
API_KEY = "$2a$10$fhgij9c5sO3ezqwOcJi0u.V7MHzvSaLRPqlOfpkziPwfZByxDc9SG" 
URL_BASE = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# 2. Diccionario base con todas las actividades
ESTADOS_POR_DEFECTO = {
    "lunes-t1": "PENDIENTE", "lunes-t2": "PENDIENTE", "lunes-t3": "PENDIENTE", "lunes-t4": "PENDIENTE", "lunes-t5": "PENDIENTE", "lunes-t6": "PENDIENTE",
    "martes-t1": "PENDIENTE", "martes-t2": "PENDIENTE", "martes-t3": "PENDIENTE", "martes-t4": "PENDIENTE", "martes-t5": "PENDIENTE", "martes-t6": "PENDIENTE",
    "miercoles-t1": "PENDIENTE", "miercoles-t2": "PENDIENTE", "miercoles-t3": "PENDIENTE", "miercoles-t4": "PENDIENTE", "miercoles-t5": "PENDIENTE", "miercoles-t6": "PENDIENTE", "miercoles-t7": "PENDIENTE", "miercoles-t8": "PENDIENTE",
    "jueves-t1": "PENDIENTE", "jueves-t2": "PENDIENTE", "jueves-t3": "PENDIENTE", "jueves-t4": "PENDIENTE", "jueves-t5": "PENDIENTE", "jueves-t6": "PENDIENTE", "jueves-t7": "PENDIENTE", "jueves-t8": "PENDIENTE",
    "viernes-t1": "PENDIENTE", "viernes-t2": "PENDIENTE", "viernes-t3": "PENDIENTE"
}

# 3. Función para LEER el estado real desde la nube
def obtener_estados_nube():
    try:
        # Petición a JSONBin para traer la última versión guardada
        url_get = f"{URL_BASE}/latest?meta=false"
        respuesta = requests.get(url_get, headers={"X-Master-Key": API_KEY}, timeout=5)
        if respuesta.status_code == 200:
            datos_nube = respuesta.json()
            # Combina con los valores por defecto si falta alguna clave
            estados_completos = {**ESTADOS_POR_DEFECTO, **datos_nube}
            return estados_completos
    except Exception as e:
        st.error(f"Error al leer datos de la nube: {e}")
    return ESTADOS_POR_DEFECTO

# 4. Función para GUARDAR cambios en la nube
def actualizar_estado_nube(nuevos_estados):
    try:
        respuesta = requests.put(URL_BASE, json=nuevos_estados, headers=HEADERS, timeout=5)
        if respuesta.status_code == 200:
            st.success("✅ Nube actualizada con éxito", icon="☁️")
        else:
            st.error(f"Error al actualizar la nube: Código {respuesta.status_code}")
    except Exception as e:
        st.error(f"Error de conexión al guardar: {e}")

# 5. Cargar datos en la sesión actual
if 'estados' not in st.session_state:
    st.session_state.estados = obtener_estados_nube()

# --- INTERFAZ DEL PANEL ---
st.title("🎛️ Panel de Control - Evento Indpulsa")
st.write("Los cambios realizados aquí se guardan en la nube y se reflejan en la web para todos.")

# Botón para sincronizar manualmente
if st.button("🔄 Sincronizar datos de la nube"):
    st.session_state.estados = obtener_estados_nube()
    st.rerun()

st.markdown("---")

# 6. Estructura de actividades organizadas por día
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

# 7. Renderizado de controles
for dia, talleres in talleres_por_dia.items():
    st.header(f"📅 {dia}")
    
    for key, nombre in talleres:
        st.subheader(f"🔹 {nombre}")
        
        # Muestra el estado que está guardado en la nube
        estado_actual = st.session_state.estados.get(key, "PENDIENTE")
        st.info(f"Estado actual: **{estado_actual}**")
        
        col1, col2, col3 = st.columns(3)
        
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
            
    st.markdown("---")