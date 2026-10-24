import streamlit as st
import time
import random
import os
import base64
from gtts import gTTS

st.set_page_config(page_title="Reloj de Sombras TT", page_icon="🏓", layout="wide")

# --- 1. Preparación de Audios en Memoria (Diccionario Base64) ---
@st.cache_data
def cargar_audios_b64():
    """Genera los mp3 y devuelve un diccionario con los audios ya convertidos a Base64."""
    golpes = {
        "drive": "Drive", 
        "reves": "Revés",
        "top_drive": "Top Drive",
        "top_reves": "Top Revés",
        "corto_drive": "Corto Drive",
        "corto_reves": "Corto Revés",
        "pivot": "Pivot",
        "freno": "Quietos",
        "intro": "Inicio de entrenamiento",
        "3": "Tres",
        "2": "Dos",
        "1": "Uno"
    }
    
    if not os.path.exists("audios"):
        os.makedirs("audios")
        
    audios_codificados = {}
    for clave, texto in golpes.items():
        archivo = f"audios/{clave}.mp3"
        if not os.path.exists(archivo):
            tts = gTTS(text=texto, lang='es', tld='com.ar')
            tts.save(archivo)
        with open(archivo, "rb") as f:
            audios_codificados[clave] = base64.b64encode(f.read()).decode()
            
    return audios_codificados

AUDIOS_B64 = cargar_audios_b64()

# --- 2. Motor Gráfico + Audio Unificado (Fuerza al navegador a reproducir siempre) ---
def renderizar_tablero(color_fondo, icono, texto, subtexto="", clave_audio=None):
    """Renderiza el tablero visual e inyecta el audio directamente en el mismo bloque DOM."""
    bloque_texto = (
        f'<div style="font-size: 4rem; font-weight: 900; color: white; font-family: sans-serif; '
        f'text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">{texto}</div>'
        if texto else ""
    )
    
    # Si hay un audio que reproducir en este fotograma, lo incrustamos con un ID irrepetible
    bloque_audio = ""
    if clave_audio and clave_audio in AUDIOS_B64:
        b64 = AUDIOS_B64[clave_audio]
        uid = f"{clave_audio}_{time.time()}"
        bloque_audio = (
            f'<audio id="{uid}" autoplay="true" style="display:none;">'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
            f'</audio>'
        )
    
    html_code = (
        f'<div style="background-color: {color_fondo}; height: 65vh; display: flex; flex-direction: column; '
        f'justify-content: center; align-items: center; border-radius: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); '
        f'padding: 20px; text-align: center; border: 4px solid rgba(255,255,255,0.2);">'
        f'<div style="font-size: 9rem; line-height: 1; margin-bottom: 10px;">{icono}</div>'
        f'{bloque_texto}'
        f'<div style="font-size: 1.8rem; font-weight: 600; color: rgba(255,255,255,0.9); margin-top: 10px; font-family: sans-serif;">{subtexto}</div>'
        f'{bloque_audio}'
        f'</div>'
    )
    return html_code

# --- 3. Catálogo de Estímulos ---
CATALOGO_ESTIMULOS = {
    "drive":       {"audio": "drive",       "texto": "DRIVE",       "icono": "➡️", "color": "#E65100"},
    "reves":       {"audio": "reves",       "texto": "REVÉS",       "icono": "⬅️", "color": "#BF360C"},
    "top_drive":   {"audio": "top_drive",   "texto": "TOP DRIVE",   "icono": "↗️", "color": "#D32F2F"},
    "top_reves":   {"audio": "top_reves",   "texto": "TOP REVÉS",   "icono": "↖️", "color": "#B71C1C"},
    "corto_drive": {"audio": "corto_drive", "texto": "CORTO DRIVE", "icono": "↘️", "color": "#1976D2"},
    "corto_reves": {"audio": "corto_reves", "texto": "CORTO REVÉS", "icono": "↙️", "color": "#0D47A1"},
    "pivot":       {"audio": "pivot",       "texto": "PIVOT DRIVE", "icono": "🔄", "color": "#F57F17"},
    "freno":       {"audio": "freno",       "texto": "¡QUIETO!",    "icono": "✋", "color": "#2E7D32"}
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

if incluir_freno:
    claves_activas.append("freno")

# --- 6. Interfaz Principal ---
st.title("🏓 Reloj de Sombras v3.2 — Reacción Visual y Auditiva")

with st.expander("📖 Ver Leyenda de Colores y Flechas"):
    st.markdown("""
    * 🟥 **ROJO (`↗️` / `↖️`):** Topspin / Ataque liftado (Derecha o Revés).
    * 🟦 **AZUL (`↘️` / `↙️`):** Corto / Push dentro de la mesa.
    * 🟧 **NARANJA (`➡️` / `⬅️`):** Golpe plano o bloqueo básico.
    * 🟨 **AMARILLO (`🔄`):** Pivotar en esquina de revés para pegar Drive.
    * 🟩 **VERDE (`✋`):** ¡Freno! Haz el split-step pero congélate sin sacar el brazo.
    """)

zona_tablero = st.empty()

zona_tablero.markdown(
    renderizar_tablero("#1E1E2E", "🏓", "LISTO PARA ENTRENAR", "Presiona el botón de abajo para iniciar"),
    unsafe_allow_html=True
)

if st.button("🔴 COMENZAR ENTRENAMIENTO", use_container_width=True):
    
    usar_voz = modo_estimulo in ["👁️+🔊 Híbrido (Visual + Voz)", "🔊 Solo Voz (Clásico)"]
    modo_solo_voz = (modo_estimulo == "🔊 Solo Voz (Clásico)")
    
    for serie in range(1, series + 1):
        ajuste = (serie - 1) * 0.15
        t_min = max(0.6, tiempo_base[0] - ajuste)
        t_max = max(1.0, tiempo_base[1] - ajuste)
        
        # 1. Aviso de Preparación
        zona_tablero.markdown(
            renderizar_tablero("#37474F", "🏓", "EN POSICIÓN...", f"Serie {serie} de {series}", clave_audio="intro"),
            unsafe_allow_html=True
        )
        time.sleep(2.2)
        
        # 2. Cuenta regresiva 3, 2, 1 sincronizada
        for seg in ["3", "2", "1"]:
            zona_tablero.markdown(
                renderizar_tablero("#263238", "⏱️", f"¡{seg}!", f"Serie {serie} de {series}", clave_audio=seg),
                unsafe_allow_html=True
            )
            time.sleep(1.0)
            
        for golpe_num in range(1, golpes_por_serie + 1):
            # Fase 1: Pantalla neutra de espera (sin audio, destruye la etiqueta <audio> anterior)
            espera = random.uniform(t_min, t_max)
            zona_tablero.markdown(
                renderizar_tablero("#121212", "⚡", "" if ocultar_texto else "SPLIT-STEP", f"Golpe {golpe_num}/{golpes_por_serie}", clave_audio=None),
                unsafe_allow_html=True
            )
            time.sleep(espera)
            
            # Fase 2: Elegir golpe y definir audio/visual
            clave_elegida = random.choice(claves_activas)
            datos_golpe = CATALOGO_ESTIMULOS[clave_elegida]
            
            # Determinar qué audio toca reproducir
            sonido_actual = None
            if usar_voz:
                if forzar_audio_corto and clave_elegida in ["top_drive", "corto_drive"]:
                    sonido_actual = "drive"
                elif forzar_audio_corto and clave_elegida in ["top_reves", "corto_reves"]:
                    sonido_actual = "reves"
                else:
                    sonido_actual = datos_golpe["audio"]
            
            # Determinar qué mostrar en pantalla (si es Solo Voz, no muestra colores para obligar a usar el oído)
            if modo_solo_voz:
                color_mostrar = "#1E1E2E"
                icono_mostrar = "🔊"
                texto_mostrar = "" if ocultar_texto else datos_golpe["texto"]
            else:
                color_mostrar = datos_golpe["color"]
                icono_mostrar = datos_golpe["icono"]
                texto_mostrar = "" if ocultar_texto else datos_golpe["texto"]
            
            # Impacto Visual + Auditivo simultáneo en el mismo contenedor
            zona_tablero.markdown(
                renderizar_tablero(
                    color_mostrar, 
                    icono_mostrar, 
                    texto_mostrar, 
                    f"Golpe {golpe_num}/{golpes_por_serie}",
                    clave_audio=sonido_actual
                ),
                unsafe_allow_html=True
            )
            
            # Pausa para que suene el audio completo antes de volver a SPLIT-STEP
            time.sleep(1.1)
            
        if serie < series:
            for d in range(10, 0, -1):
                zona_tablero.markdown(
                    renderizar_tablero("#004D40", "🧘‍♂️", f"DESCANSO: {d}s", f"Serie {serie} completada", clave_audio=None),
                    unsafe_allow_html=True
                )
                time.sleep(1)
                
    zona_tablero.markdown(
        renderizar_tablero("#1B5E20", "🎉", "¡ENTRENAMIENTO TERMINADO!", "Excelente velocidad de reacción", clave_audio=None),
        unsafe_allow_html=True
    )