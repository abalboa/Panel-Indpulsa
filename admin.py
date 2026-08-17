import streamlit as st
import requests

# 1. Configuración de credenciales de JSONBin
BIN_ID = "6a7566a3da38895dfec48c54"  
API_KEY = "$2a$10$fhgij9c5sO3ezqwOcJi0u.V7MHzvSaLRPqlOfpkziPwfZByxDc9SG" 
URL_BASE = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS_GET = {
    "X-Master-Key": API_KEY,
    "X-Bin-Meta": "false"
}

HEADERS_PUT = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY,
    "X-Bin-Versioning": "false"
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
        url_get = f"{URL_BASE}/latest"
        respuesta = requests.get(url_get, headers=HEADERS_GET, timeout=15)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            # Si JSONBin viene envuelto en "record", lo extraemos
            if isinstance(datos, dict) and "record" in datos:
                datos = datos["record"]
            
            # Combinamos asegurando todas las llaves
            estados_limpios = {k: datos.get(k, "PENDIENTE") for k in ESTADOS_POR_DEFECTO}
            return estados_limpios
        else:
            st.error(f"Error al leer de JSONBin ({respuesta.status_code}): {respuesta.text}")
    except Exception as e:
        st.error(f"Error de conexión al leer: {e}")
    return ESTADOS_POR_DEFECTO

# 4. Función para GUARDAR cambios en la nube
def guardar_cambio(key, nuevo_estado):
    st.session_state.estados[key] = nuevo_estado
    
    # Enviamos solo las claves limpias
    payload = {k: st.session_state.estados[k] for k in ESTADOS_POR_DEFECTO}
    
    try:
        respuesta = requests.put(URL_BASE, json=payload, headers=HEADERS_PUT, timeout=15)
        if respuesta.status_code == 200:
            st.toast(f"✅ {key} actualizado a {nuevo_estado}", icon="☁️")
        else:
            st.error(f"❌ Error al guardar en JSONBin ({respuesta.status_code}): {respuesta.text}")
    except Exception as e:
        st.error(f"❌ Error de conexión al guardar: {e}")

# 5. Cargar datos en la sesión
if 'estados' not in st.session_state:
    st.session_state.estados = obtener_estados_nube()

# --- INTERFAZ DEL PANEL ---
st.title("🎛️ Panel de Control - Evento Indpulsa")
st.write("Los cambios realizados aquí se guardan en la nube y se reflejan en la web para todos.")

# Botón para forzar sincronización
if st.button("🔄 Sincronizar datos de la nube"):
    st.session_state.estados = obtener_estados_nube()
    st.rerun()

st.markdown("---")

# 6. Estructura de actividades
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
        
        estado_actual = st.session_state.estados.get(key, "PENDIENTE")
        st.info(f"Estado actual: **{estado_actual}**")
        
        col1, col2, col3 = st.columns(3)
        
        if col1.button("🕒 Pendiente", key=f"btn_p_{key}"):
            guardar_cambio(key, "PENDIENTE")
            st.rerun()

        if col2.button("▶️ En Proceso", key=f"btn_e_{key}"):
            guardar_cambio(key, "EN PROCESO")
            st.rerun()

        if col3.button("✅ Finalizado", key=f"btn_f_{key}"):
            guardar_cambio(key, "FINALIZADO")
            st.rerun()
            
    st.markdown("---")