import streamlit as st
import requests
import time

# 1. Configuración de credenciales de JSONBin
BIN_ID = "6a7566a3da38895dfec48c54"  
API_KEY = "$2a$10$fhgij9c5sO3ezqwOcJi0u.V7MHzvSaLRPqlOfpkziPwfZByxDc9SG" 
URL_BIN = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# 2. Diccionario base por si el Bin está completamente vacío
ESTADOS_POR_DEFECTO = {
    "lunes-t1": "PENDIENTE", "lunes-t2": "PENDIENTE", "lunes-t3": "PENDIENTE", "lunes-t4": "PENDIENTE", "lunes-t5": "PENDIENTE", "lunes-t6": "PENDIENTE",
    "martes-t1": "PENDIENTE", "martes-t2": "PENDIENTE", "martes-t3": "PENDIENTE", "martes-t4": "PENDIENTE", "martes-t5": "PENDIENTE", "martes-t6": "PENDIENTE",
    "miercoles-t1": "PENDIENTE", "miercoles-t2": "PENDIENTE", "miercoles-t3": "PENDIENTE", "miercoles-t4": "PENDIENTE", "miercoles-t5": "PENDIENTE", "miercoles-t6": "PENDIENTE", "miercoles-t7": "PENDIENTE", "miercoles-t8": "PENDIENTE",
    "jueves-t1": "PENDIENTE", "jueves-t2": "PENDIENTE", "jueves-t3": "PENDIENTE", "jueves-t4": "PENDIENTE", "jueves-t5": "PENDIENTE", "jueves-t6": "PENDIENTE", "jueves-t7": "PENDIENTE", "jueves-t8": "PENDIENTE",
    "viernes-t1": "PENDIENTE", "viernes-t2": "PENDIENTE", "viernes-t3": "PENDIENTE"
}

# 3. Función robusta para LEER con auto-reintento
def leer_nube():
    for intento in range(2): # Reintenta hasta 2 veces si hay lentitud
        try:
            # Usamos ?meta=false directamente en la URL para máxima compatibilidad
            res = requests.get(f"{URL_BIN}?meta=false", headers={"X-Master-Key": API_KEY}, timeout=10)
            if res.status_code == 200:
                datos = res.json()
                # Extrae el record si viene empaquetado
                if isinstance(datos, dict) and "record" in datos:
                    datos = datos["record"]
                return {**ESTADOS_POR_DEFECTO, **datos}
        except Exception:
            time.sleep(1) # Pequeña pausa antes de reintentar
    return None

# 4. Función de GUARDADO ATÓMICO (Lee lo último, cambia solo una clave y guarda)
def guardar_cambio_en_nube(clave_actividad, nuevo_estado):
    with st.spinner(f"Actualizando {clave_actividad}..."):
        # Paso 1: Traemos el estado real más reciente de la nube
        datos_actuales = leer_nube()
        if datos_actuales is None:
            st.error("❌ No se pudo conectar con la nube para guardar. Revisa tu conexión.")
            return False

        # Paso 2: Modificamos SOLAMENTE la actividad presionada
        datos_actuales[clave_actividad] = nuevo_estado

        # Paso 3: Guardamos la base de datos completa y actualizada
        try:
            res = requests.put(URL_BIN, json=datos_actuales, headers=HEADERS, timeout=12)
            if res.status_code == 200:
                st.session_state.estados = datos_actuales
                st.toast(f"✅ Guardado: {clave_actividad} -> {nuevo_estado}", icon="☁️")
                return True
            else:
                st.error(f"❌ Error de JSONBin ({res.status_code}): {res.text}")
        except Exception as e:
            st.error(f"❌ Error de conexión al guardar: {e}")
    return False

# 5. Cargar datos en la aplicación
if 'estados' not in st.session_state or st.session_state.estados is None:
    estados_cargados = leer_nube()
    if estados_cargados:
        st.session_state.estados = estados_cargados
    else:
        st.session_state.estados = ESTADOS_POR_DEFECTO

# --- INTERFAZ DEL PANEL ---
st.title("🎛️ Panel de Control - Evento Indpulsa")

col_info, col_btn = st.columns([3, 1])
with col_info:
    st.caption("🟢 Conectado con la base de datos en tiempo real.")
with col_btn:
    if st.button("🔄 Refrescar Nube"):
        st.session_state.estados = leer_nube()
        st.rerun()

st.markdown("---")

# 6. Estructura de las actividades organizadas por día
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
        
        # Color visual del estado actual en el panel
        if estado_actual == "EN PROCESO":
            st.info(f"Estado actual: **{estado_actual}**")
        elif estado_actual == "FINALIZADO":
            st.success(f"Estado actual: **{estado_actual}**")
        else:
            st.write(f"Estado actual: **{estado_actual}**")
        
        col1, col2, col3 = st.columns(3)
        
        if col1.button("🕒 Pendiente", key=f"btn_p_{key}"):
            if guardar_cambio_en_nube(key, "PENDIENTE"):
                st.rerun()

        if col2.button("▶️ En Proceso", key=f"btn_e_{key}"):
            if guardar_cambio_en_nube(key, "EN PROCESO"):
                st.rerun()

        if col3.button("✅ Finalizado", key=f"btn_f_{key}"):
            if guardar_cambio_en_nube(key, "FINALIZADO"):
                st.rerun()
            
    st.markdown("---")