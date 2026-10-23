import streamlit as st
import time
import random
import os
import base64
from gtts import gTTS

st.set_page_config(page_title="Reloj de Sombras TT", page_icon="🏓", layout="wide")

# --- 1. Preparación de Audios ---
@st.cache_data
def preparar_audios():
    golpes = {
        "drive": "Drive", 
        "reves": "Revés",
        "top_drive": "Top Drive",
        "top_reves": "Top Revés",
        "corto_drive": "Corto Drive",
        "corto_reves": "Corto Revés",
        "pivot": "Pivot",
        "freno": "Quietos",
        "countdown": "Inicio de entrenamiento en 3... 2... 1..."
    }
    
    if not os.path.exists("audios"):
        os.makedirs("audios")
        
    for clave, texto in golpes.items():
        archivo = f"audios/{clave}.mp3"
        if not os.path.exists(archivo):
            tts = gTTS(text=texto, lang='es', tld='com.ar')
            tts.save(archivo)
            
preparar_audios()

def reproducir_audio(clave):
    """Inyecta el reproductor HTML5 oculto."""
    archivo = f"audios/{clave}.mp3"
    with open(archivo, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.empty().markdown(audio_html, unsafe_allow_html=True)

# --- 2. Motor Gráfico del Tablero Visual (CSS Dinámico) ---
def renderizar_tablero(color_fondo, icono, texto, subtexto=""):
    """Crea una tarjeta gigante de alto contraste para ver desde lejos."""
    html_code = f"""
    <div style="
        background-color: {color_fondo};
        height: 65vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        transition: background-color 0.05s ease;
        padding: 20px;
        text-align: center;
        border: 4px solid rgba(255,255,255,0.2);
    ">
        <div style="font-size: 9rem; line-height: 1; margin-bottom: 10px;">{icono}</div>
        <div style="font-size: 4rem; font-weight: 900; color: white; font-family: sans-serif; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">
            {texto}
        </div>
        <div style="font-size: 1.8rem; font-weight: 600; color: rgba(255,255,255,0.9); margin-top: 10px; font-family: sans-serif;">
            {subtexto}
        </div>
    </div>
    """
    return html_code

# --- 3. Base de Datos de Estímulos Visuales y Auditivos ---
# Diccionario con toda la configuración visual de cada golpe
CATALOGO_ESTIMULOS = {
    "drive":       {"audio": "drive",       "texto": "DRIVE",       "icono": "➡️", "color": "#E65100"}, # Naranja
    "reves":       {"audio": "reves",       "texto": "REVÉS",       "icono": "⬅️", "color": "#BF360C"}, # Naranja oscuro
    "top_drive":   {"audio": "top_drive",   "texto": "TOP DRIVE",   "icono": "↗️", "color": "#D32F2F"}, # Rojo intenso
    "top_reves":   {"audio": "top_reves",   "texto": "TOP REVÉS",   "icono": "↖️", "color": "#B71C1C"}, # Rojo sangre
    "corto_drive": {"audio": "corto_drive", "texto": "CORTO DRIVE", "icono": "↘️", "color": "#1976D2"}, # Azul
    "corto_reves": {"audio": "corto_reves", "texto": "CORTO REVÉS", "icono": "↙️", "color": "#0D47A1"}, # Azul marino
    "pivot":       {"audio": "pivot",       "texto": "PIVOT DRIVE", "icono": "🔄", "color": "#F57F17"}, # Amarillo/Oro
    "freno":       {"audio": "freno",       "texto": "¡QUIETO!",    "icono": "✋", "color": "#2E7D32"}  # Verde (Inhibición)
}

# --- 4. Barra Lateral de Configuración ---
st.sidebar.header("⚙️ Configuración")

modo_estimulo = st.sidebar.radio(
    "Modo de Estímulo",
    ["👁️ Solo Visual (Silencioso)", "👁️+🔊 Híbrido (Visual + Voz)", "🔊 Solo Voz (Clásico)"]
)

categoria = st.sidebar.selectbox(
    "Categoría de Trabajo",
    ["Básico", "Topspin", "Corto", "Ataque + Pivot", "Mixto Total"]
)

incluir_freno = st.sidebar.checkbox("Añadir Trampa Visual (Verde = No moverse)", value=True)
ocultar_texto = st.sidebar.checkbox("Modo Pro: Ocultar texto (Solo flechas y color)", value=False)

series = st.sidebar.number_input("Cantidad de Series", 1, 10, 3)
golpes_por_serie = st.sidebar.number_input("Golpes por Serie", 5, 50, 20)
tiempo_base = st.sidebar.slider("Tiempo entre golpes (seg)", 0.8, 4.0, (1.5, 2.8))

# --- 5. Selección de Golpes Activos ---
if categoria == "Básico":
    claves_activas = ["drive", "reves"]
    forzar_audio_corto = True
elif categoria == "Topspin":
    claves_activas = ["top_drive", "top_reves"]
    forzar_audio_corto = True
elif categoria == "Corto":
    claves_activas = ["corto_drive", "corto_reves"]
    forzar_audio_corto = True
elif categoria == "Ataque + Pivot":
    claves_activas = ["top_drive", "top_reves", "pivot"]
    forzar_audio_corto = False
else:
    claves_activas = ["drive", "reves", "top_drive", "top_reves", "corto_drive", "corto_reves", "pivot"]
    forzar_audio_corto = False

# Si activó la trampa de inhibición, agregamos el "freno" con menor probabilidad
if incluir_freno:
    claves_activas.append("freno")

# --- 6. Interfaz Principal ---
st.title("🏓 Reloj de Sombras v3.0 — Reacción Visual")

with st.expander("📖 Ver Leyenda de Colores y Flechas"):
    st.markdown("""
    * 🟥 **ROJO (`↗️` / `↖️`):** Topspin / Ataque liftado (Derecha o Revés).
    * 🟦 **AZUL (`↘️` / `↙️`):** Corto / Push dentro de la mesa.
    * 🟧 **NARANJA (`➡️` / `⬅️`):** Golpe plano o bloqueo básico.
    * 🟨 **AMARILLO (`🔄`):** Pivotar en esquina de revés para pegar Drive.
    * 🟩 **VERDE (`✋`):** ¡Freno! Haz el split-step pero congélate sin sacar el brazo.
    """)

zona_estado = st.empty()
zona_tablero = st.empty()

# Mostrar tablero en estado de reposo antes de empezar
zona_tablero.markdown(
    renderizar_tablero("#1E1E2E", "🏓", "LISTO PARA ENTRENAR", "Presiona el botón de abajo para iniciar"),
    unsafe_allow_html=True
)

if st.button("🔴 COMENZAR ENTRENAMIENTO", use_container_width=True):
    
    for serie in range(1, series + 1):
        ajuste = (serie - 1) * 0.15
        t_min = max(0.6, tiempo_base[0] - ajuste)
        t_max = max(1.0, tiempo_base[1] - ajuste)
        
        # Cuenta regresiva
        reproducir_audio("countdown")
        for seg in ["3", "2", "1"]:
            zona_tablero.markdown(
                renderizar_tablero("#37474F", "⏱️", f"PREPARADO... {seg}", f"Serie {serie} de {series}"),
                unsafe_allow_html=True
            )
            time.sleep(1.3)
            
        for golpe_num in range(1, golpes_por_serie + 1):
            # 1. Pantalla neutra (Espera en posición base / Split-Step)
            espera = random.uniform(t_min, t_max)
            zona_tablero.markdown(
                renderizar_tablero("#121212", "⚡", "SPLIT-STEP", f"Golpe {golpe_num}/{golpes_por_serie}"),
                unsafe_allow_html=True
            )
            time.sleep(espera)
            
            # 2. Elegir golpe y obtener sus propiedades visuales
            clave_elegida = random.choice(claves_activas)
            datos_golpe = CATALOGO_ESTIMULOS[clave_elegida]
            
            texto_mostrar = "" if ocultar_texto else datos_golpe["texto"]
            
            # 3. Impacto Visual (Flash de color y flecha)
            zona_tablero.markdown(
                renderizar_tablero(
                    datos_golpe["color"], 
                    datos_golpe["icono"], 
                    texto_mostrar, 
                    f"Golpe {golpe_num}/{golpes_por_serie}"
                ),
                unsafe_allow_html=True
            )
            
            # 4. Impacto Auditivo (si corresponde según el modo elegido)
            if modo_estimulo != "👁️ Solo Visual (Silencioso)":
                if forzar_audio_corto and clave_elegida in ["top_drive", "corto_drive"]:
                    reproducir_audio("drive")
                elif forzar_audio_corto and clave_elegida in ["top_reves", "corto_reves"]:
                    reproducir_audio("reves")
                else:
                    reproducir_audio(datos_golpe["audio"])
            
            # Tiempo que permanece el color en pantalla antes de volver a negro
            time.sleep(0.85)
            
        if serie < series:
            for d in range(10, 0, -1):
                zona_tablero.markdown(
                    renderizar_tablero("#004D40", "🧘‍♂️", f"DESCANSO: {d}s", f"Serie {serie} completada"),
                    unsafe_allow_html=True
                )
                time.sleep(1)
                
    zona_tablero.markdown(
        renderizar_tablero("#1B5E20", "🎉", "¡ENTRENAMIENTO TERMINADO!", "Excelente velocidad de reacción"),
        unsafe_allow_html=True
    )